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
# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring, unused-argument

import unittest
import logging
from unittest import mock
from .chat_client import ChatClient


class ChatClientTest(unittest.TestCase):

    def setUp(self):
        logging.getLogger().setLevel(logging.CRITICAL)

    def tearDown(self):
        logging.getLogger().setLevel(logging.INFO)

    @mock.patch("click.echo")
    @mock.patch("click.secho")
    def test_chat_client(self, mock_secho, mock_echo):
        client = ChatClient("physics_expert")
        client.process_input("Tell me about the double-slit experiment.")
        client.handle_command("feedback Talk like a prirate")
        client.handle_command("principles")


if __name__ == "__main__":
    unittest.main()
