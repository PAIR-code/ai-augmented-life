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
from utils.test_utils import build_message_history_for_test
from .agents import AgentState
from .fake_agent import FakeAgent


class TestFakeAgent(unittest.TestCase):
    def test_chat(self):
        agent = FakeAgent()
        message_history = build_message_history_for_test([])
        response, world_state = agent.chat(AgentState("Hello", message_history, None))
        self.assertEqual(response, "Fake response to message 0: Hello")
        self.assertEqual(world_state, {"last_message": "Hello", "message_count": 0})

        message_history = build_message_history_for_test(
            ["Hello", response, "How are you?"]
        )
        response, world_state = agent.chat(
            AgentState("How are you?", message_history, world_state)
        )
        self.assertEqual(response, "Fake response to message 3: How are you?")
        self.assertEqual(
            world_state, {"last_message": "How are you?", "message_count": 3}
        )


if __name__ == "__main__":
    unittest.main()
