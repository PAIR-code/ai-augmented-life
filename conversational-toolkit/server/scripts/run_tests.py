# Copyright 2024 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# pylint: disable=line-too-long, consider-using-dict-items, consider-using-with
# pylint: disable=too-few-public-methods, consider-iterating-dictionary, no-value-for-parameter

"""
Helper for running unit tests multiple times in order to assess overall
success rate.

*WARNING*: This script is designed to make multiple API calls to the LLM model
and can incur significant costs.

Usage: 
    python3 -m server.scripts.run_tests --test_name=fake_agent_test --run_count=1 --max_threads=5
"""
import os
import threading
import time
import concurrent.futures

import unittest
import click

from dotenv import load_dotenv
import rich
from rich.panel import Panel

# Nb: See https://github.com/langchain-ai/langchain/issues/20929
# Due to a bug in google.cloud.aiplatform this will fail for
# vertex ai if THREADS > 1. Use the patch described in the thread
# above until an official fix is available.
DEFAULT_MAX_THREADS = 5
DEFAULT_TEST_NAME = "fake_agent_test"
DEFAULT_RUN_COUNT = 1


class _TraceLogEntry:
    def __init__(self, test, result):
        self.test = test
        self.result = result

    def __str__(self):
        return f"{self.test.id()}: {self.result}"


@click.command()
@click.option(
    "--test_name",
    help="Name of the test suite and (optionally) the test case in the \
        format 'suite.TestCase'",
)
@click.option(
    "--run_count",
    default=DEFAULT_RUN_COUNT,
    help="Number of times to run each test or test suite",
)
@click.option(
    "--max_threads",
    default=DEFAULT_MAX_THREADS,
    help="Maximum number of parallel threads to use when running the \
        tests",
)
def _run_tests(test_name, run_count, max_threads):
    """Executes specified tests in parallel, running each test run_count times.

    Args:
        test_name (str): Name of the test (either a test suite or a specific test case within a suite).
        run_count (int): Number of times to repeat each test.
        max_threads (int): Maximum number of threads to use for parallel execution.
    Returns:
        None.
    """
    if not test_name:
        click.secho(
            f"Warning: No test name provided, using default \
                {DEFAULT_TEST_NAME}. There will be no LLM apis \
                calls for this test.",
            fg="yellow",
        )
        test_name = DEFAULT_TEST_NAME
    elif test_name == "all":
        click.secho("Running all unit tests...", fg="green")
        _run_all_tests(max_threads=max_threads)
        return

    click.secho(
        f"Running tests for '{test_name}, repeating {run_count} times with {max_threads} threads.'",
        fg="yellow",
    )

    test_suite = test_name.split(".")[0] if "." in test_name else test_name
    test_case = test_name.split(".")[1] if "." in test_name else None

    suite = _find_test_file(test_suite)
    if suite.countTestCases() == 0:
        click.secho(f"No test file found for '{test_name}'", fg="red")
        return

    if test_case is None:
        click.secho(f"Running all tests in '{test_suite}'", fg="green")
    else:
        click.secho(f"Running test case '{test_case}' in '{test_suite}'", fg="green")

    all_tests = _get_all_tests_from_suite(suite)
    filtered_tests = []
    for test in all_tests:
        if test_case is None or test.id().endswith(test_case):
            for _ in range(run_count):
                filtered_tests.append(test)

    _run_in_parallel(filtered_tests, max_threads)


def _run_in_parallel(tests, max_threads):

    runner = unittest.TextTestRunner(stream=open(os.devnull, "w", encoding="utf-8"))
    trace_log = []

    progress = 0
    progress_lock = threading.Lock()

    with click.progressbar(length=len(tests), label="Running tests") as progress_bar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            executor.map(lambda test: _run_test(test, runner, trace_log), tests)

            while progress < len(tests):
                with progress_lock:
                    progress_bar.update(len(trace_log) - progress)
                    progress = len(trace_log)
                    time.sleep(0.1)

            executor.shutdown()
            _process_results(trace_log)


def _run_test(test, runner, trace_log):
    trace_log.append(_TraceLogEntry(test, runner.run(test)))


def _run_all_tests(
    start_dir="server",
    pattern="*_test.py",
    top_level_dir=".",
    max_threads=DEFAULT_MAX_THREADS,
):
    """Discovers and runs all test files matching the pattern in the directory tree.
    Equivalent to: `python3 -m unittest discover -t .. -s . -p "*_test.py"`

    Args:
        start_dir: The directory to start the discovery from (defaults to current dir).
        pattern: The filename pattern to match test files (defaults to "*_test.py").
        top_level_dir: The top-level directory of the project (used for module loading).
    """
    loader = unittest.TestLoader()
    top_level_dir = os.path.abspath(os.path.join(start_dir, ".."))
    suite = loader.discover(start_dir, pattern=pattern, top_level_dir=top_level_dir)
    all_tests = _get_all_tests_from_suite(suite)
    _run_in_parallel(all_tests, max_threads)


def _get_all_tests_from_suite(suite):
    """Recursively extracts all TestCase objects from a TestSuite."""
    tests = []
    for test in suite:
        if isinstance(test, unittest.TestCase):  # Check if it's a TestCase
            tests.append(test)
        else:
            tests.extend(
                _get_all_tests_from_suite(test)
            )  # Recurse if it's another TestSuite
    return tests


def _process_results(trace_log):
    result_map = {}
    for result_entry in trace_log:
        test_id = result_entry.test.id()

        if test_id in result_map:
            result_map[test_id].append(result_entry.result)
        else:
            result_map[test_id] = [result_entry.result]

    for test_id in result_map.keys():
        click.secho(f"\n\n----------------- {test_id} -----------------", fg="blue")
        passed = 0
        failed = 0
        errors = 0

        failed_list = []
        errors_list = []
        for result in result_map[test_id]:
            if result.wasSuccessful():
                passed += 1
            elif len(result.errors) > 0:
                errors += len(result.errors)
                errors_list.extend(result.errors)
            else:
                failed += len(result.failures)
                failed_list.extend(result.failures)

        total_tests = passed + failed + errors
        percentage_passed = round((passed / total_tests) * 100)
        click.secho(f"Tests passed: {passed} ({percentage_passed}%)", fg="green")
        click.secho(f"Tests failed: {failed}", fg="red")

        if failed > 0:
            content = "\n\n".join([failure[1] for failure in failed_list])
            panel = Panel(content, title="Failure details", expand=False)
            rich.print(panel)

        click.secho(f"Tests with errors: {errors}", fg="red")
        if errors > 0:
            content = ""
            for error in errors_list:
                content += f"{error[0]}\n{error[1]}\n\n"

            panel = Panel(content, title="Failure details", expand=False)
            rich.print(panel)


def _find_test_file(test_module):
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=".", pattern=f"{test_module}.py")
    return suite


if __name__ == "__main__":
    load_dotenv()
    _run_tests()
