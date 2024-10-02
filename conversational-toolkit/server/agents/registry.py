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

"""
Registry for all agents supported by the server. New agents should be added to
_AGENT_BY_ID to allow the server to call them.
"""
from typing import Dict, Final, Type
from .agents import ConversationalAgent
from .default_agent import DefaultAgent
from .fake_agent import FakeAgent
from .history_tutor.history_tutor import HistoryTutor
from .physics_expert.physics_expert import PhysicsExpert
from .the_coordination_game.the_coordination_game import CoordinationGame


# Create conversational agents. An agent is a ConversationalAgent subclass.
# It's able to respond to user messages based on the conversation history
# and previous state.
# New agents should be registered here.
_AGENT_BY_ID: Final[Dict[str, Type[ConversationalAgent]]] = {
    "default": DefaultAgent,
    "fake": FakeAgent,
    "history_tutor": HistoryTutor,
    "physics_expert": PhysicsExpert,
    "coordination_game": CoordinationGame,
}

# Dict to keep track of instantiated agents.
_ACTIVE_AGENT_BY_ID: Final[Dict[str, Type[ConversationalAgent]]] = {}


class AgentRegistry:
    """A registry for ConversationalAgents.
    This class provides a way to retrieve ConversationalAgents by id.
    """

    def get_agent(self, agent_id: str) -> ConversationalAgent:
        """Retrieves a ConversationalAgent by id. Instantiates agent obejcts
        lazily.

        Args:
            agent_id: The id of the agent to retrieve.
        Returns:
            The ConversationalAgent object.
        Raises:
            ValueError: If the agent id is not registered.
        """
        if agent_id not in _AGENT_BY_ID:
            raise ValueError(f"agent '{agent_id}' not registered.")

        if agent_id in _ACTIVE_AGENT_BY_ID:
            return _ACTIVE_AGENT_BY_ID[agent_id]

        return _AGENT_BY_ID[agent_id]()

    def is_agent_registered(self, agent_id: str) -> bool:
        """Checks if an agent is registered.

        Args:
            agent_id: The id of the agent to check.
        Returns:
            True if the agent is registered, False otherwise.
        """
        return agent_id in _AGENT_BY_ID

    def list_agents(self) -> list[str]:
        """Returns a list of registered agent ids.

        Returns:
            list[str]: List of agent ids.
        """
        return list(_AGENT_BY_ID.keys())
