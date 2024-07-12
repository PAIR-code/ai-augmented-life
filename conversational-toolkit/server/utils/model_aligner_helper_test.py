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
# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring
import unittest
from model_alignment import single_run
from .model_aligner_helper import VertexModelHelper


class TestModelAlignerHelper(unittest.TestCase):
    def test_vertex_helper(self):
        vertex = VertexModelHelper()
        result = vertex.predict("Tell me a joke", 0.5, candidate_count=1)
        self.assertIsNotNone(result)

    def test_generates_principles(self):
        single_run_prompt = single_run.AlignableSingleRun(VertexModelHelper())
        initial_prompt = "Tell me a joke about {topic}."
        single_run_prompt.set_model_description(initial_prompt)
        _ = single_run_prompt.send_input({"topic": "fish"})
        principles = single_run_prompt.critique_response("Not funny enough.")
        self.assertIsNotNone(principles)
        single_run_prompt.update_model_description_from_principles()

        model_description = single_run_prompt.get_model_description_with_principles()
        self.assertTrue(principles[0] in model_description)
