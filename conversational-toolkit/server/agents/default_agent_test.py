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
import time
import unittest
from langchain_google_vertexai import VertexAI
from utils.test_utils import evaluate, send_chat

from .default_agent import DefaultAgent


class DefaultAgentTest(unittest.TestCase):

    def setUp(self):
        self.llm = VertexAI(model_name="gemini-pro")

    def test_chat(self):
        agent = DefaultAgent()

        transcript = [
            "Hello",
            "Hello yourself",
            "What time is it?",
        ]

        now = time.strftime("%I:%M %p")

        response, _ = send_chat(agent, transcript, None)
        success = evaluate(
            transcript,
            response,
            guidance=f"Convey correct time {now} in any human readable format.\
            Accept a response that is within 5 minutes of the correct time.",
            examples=[
                f"It's {now}",
                f"It's almost {now}. What can I help you with?",
                f"It's a little after {now}. \n\nAnything else I can help you with?",
            ],
            verbose=False,
        )

        self.assertTrue(
            success, f"Evaluation of model response failed. Response was: {response}"
        )

    def test_chat_like_a_pirate(self):
        agent = DefaultAgent()
        agent.set_fake_time_for_test("12:05 PM")
        transcript = [
            "Hello",
            "Hello yourself",
            "Tell me what time it is in the style of a pirate, but make sure\
             you're accurate to the minute.",
        ]

        response, _ = send_chat(agent, transcript, None)
        success = evaluate(
            transcript,
            response,
            guidance="Should convey the correct time (12:05 PM) in the style\
                of a pirate in any human readable format.",
            examples=[
                "Aye, it be five minutes past the midday hour, matey!",
                "Ahoy matey! It be 12:05 PM!",
            ],
            verbose=False,
        )

        self.assertTrue(
            success, f"Evaluation of model response failed. Response was: {response}"
        )
