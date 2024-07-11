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

import logging
import unittest
from langchain_google_vertexai import VertexAI
from utils.test_utils import evaluate, send_chat
from .physics_expert import PhysicsExpert


class PhysicsExpertTest(unittest.TestCase):

    def setUp(self):
        self.llm = VertexAI(model_name="gemini-pro")
        logging.getLogger().setLevel(logging.CRITICAL)

    def tearDown(self):
        logging.getLogger().setLevel(logging.INFO)

    def test_low_intensity(self):
        agent = PhysicsExpert()
        transcript = [
            "I've been reading about the double-slit \
                experiment, can you help me understand \
                it better?",
            "Sure.",
            "What evidence is there that only a single \
                photon is passing through the detector \
                at a time?",
        ]

        response, _ = send_chat(agent, transcript, None)
        success = evaluate(
            transcript,
            response,
            guidance="Explain what happens when using a low intensity \
                light source.",
            examples=[
                "When using a low intensity light source, the light is \
                so dim that only one photon passes through the detector \
                at a time. This is how we know that light is a particle.",
            ],
            verbose=False,
        )

        self.assertTrue(
            success, f"Evaluation of model response failed. Response was: {response}"
        )
