/**
 * Copyright 2024 Google LLC.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// Identifies the agent used in a conversation.
// Add new agents here. The agent ID must match the agent_id defined
// in server/agents/registry.py
export const AGENT_IDS = [
  'default',
  'fake',
  'history_tutor',
  'physics_expert',
  'coordination_game',
] as const;
export type AgentId = (typeof AGENT_IDS)[number];

// Represents a stateful conversational agent.
export interface Agent {
  // Updates the agent state following a conversation exchange.
  processExchange(state: AgentState): AgentState;
}

// Represents a generic agent state.
export interface AgentState {
  messageHistory: ChatMessage[];
  worldState: unknown | null;
}

// Represents a message in a conversation.
export interface ChatMessage {
  author: 'human' | 'ai';
  content: string;
}
