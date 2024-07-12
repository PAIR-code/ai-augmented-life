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

"""Base class for all agents."""
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Tuple
from langchain_core.messages import BaseMessage


MessageHistory = List[BaseMessage]
WorldState = dict[str, Any]


@dataclass
class AgentState:
    """Represents the internal state of a conversational agent."""

    message: str
    message_history: MessageHistory
    world_state: WorldState


AgentResponse = Tuple[str, AgentState]


class ConversationalAgent(metaclass=ABCMeta):
    """Base class for conversational AI agents."""

    def __init__(self) -> None:
        self._state: AgentState = None

    @abstractmethod
    def chat(self, agent_state: AgentState) -> AgentResponse:
        """Handles a single message exchange with the conversational agent.

        Args:
            message: incoming user message.
        Returns:
            The agent's response message.
        """

    def get_system_prompt(self) -> str:
        """Returns the main (conversational) system prompt for the agent.
        This is only needed in order to use interactive alignment tools
        in the chat_client script.
        """
        return None
