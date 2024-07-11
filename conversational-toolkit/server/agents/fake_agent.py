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

"""Fake agent with canned responses and no LLM calls."""
from .agents import AgentResponse, ConversationalAgent


class FakeAgent(ConversationalAgent):
    """Fake agent for testing that always returns a canned response and world_state."""

    def chat(self, agent_state) -> AgentResponse:
        message_count = len(agent_state.message_history)
        message = agent_state.message
        world_state = agent_state.world_state
        if world_state is None:
            world_state = self._create_initial_world_state(message, message_count)
        else:
            world_state["last_message"] = message
            world_state["message_count"] = message_count

        return (f"Fake response to message {message_count}: {message}", world_state)

    def _create_initial_world_state(self, last_message, message_count):
        return {
            "last_message": last_message,
            "message_count": message_count,
        }
