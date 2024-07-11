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

import json
import logging
import unittest

from main import app, build_message_history


# Create a test class for the build_message_history function
class TestMain(unittest.TestCase):

    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        logging.getLogger().setLevel(logging.CRITICAL)

    def tearDown(self):
        self.ctx.pop()
        logging.getLogger().setLevel(logging.INFO)

    def test_no_world_state(self):
        req = {
            "q": "user message",
            "agent_id": "fake",
        }
        resp = self.client.post("/chat", data=req)
        data = json.loads(resp.get_data())

        self.assertEqual(data["response"], "Fake response to message 0: user message")
        self.assertEqual(data["world_state"]["last_message"], "user message")

    def test_world_state_round_trip(self):
        req = {
            "q": "user message 1",
            "agent_id": "fake",
            "worldstate": "[]",
        }
        resp = self.client.post("/chat", data=req)
        data = json.loads(resp.get_data())
        world_state = data["world_state"]

        next_req = {
            "q": "user message 2",
            "agent_id": "fake",
            "world_state": json.dumps(world_state),
        }

        resp2 = self.client.post("/chat", data=next_req)
        data2 = json.loads(resp2.get_data())
        world_state2 = data2["world_state"]
        self.assertEqual(world_state2["last_message"], "user message 2")

    def test_invalid_history(self):
        incoming_messages = "xxx"
        try:
            build_message_history(incoming_messages)
            self.fail("Should have thrown an exception")
        except ValueError:
            pass


if __name__ == "__main__":
    unittest.main()
