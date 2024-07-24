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

# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring, line-too-long

import json
import unittest
from utils.test_utils import send_chat
from .empathai_agent import EmpathaiAgent


SCRIPT = [
    "I'm doctor Smith, and I've got the results of your memory tests.",
    "I've done a thorough assessment and I think you have Alzheimer's disease",
    "I've referred you to dementia support, they can give you lots of advice about coping with Alzheimer's and ways you can get support.",
    "Unfortunately there's no cure, but there are treatments that can slow down the progression.",
]


class TestEmpathaiAgent(unittest.TestCase):
    def test_teacher_marks(self):
        agent = EmpathaiAgent()
        transcript = ["Hello", "Hello doctor", SCRIPT[0]]

        _, state = send_chat(agent, transcript, None)

        # Pretty print the state object as JSON
        print(json.dumps(state, indent=4))

        self.assertGreaterEqual(state["introduces_purpose_of_conversation"], 1)
        self.assertEqual(state["uses_warning_shot"], 0)


if __name__ == "__main__":
    unittest.main()
