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

import {Component} from '@angular/core';
import {Agent, AgentState} from '@data/agent';

interface FakeAgentWorldState {
  last_message: string;
  message_count: number;
}

function isValidWorldState(state: unknown): state is FakeAgentWorldState {
  return (
    state !== null &&
    typeof state === 'object' &&
    'last_message' in state &&
    'message_count' in state
  );
}

@Component({
  selector: 'app-fake-agent',
  templateUrl: './fake-agent.component.html',
  styleUrl: './fake-agent.component.css',
})
export class FakeAgentComponent implements Agent {
  private worldState: FakeAgentWorldState = {
    last_message: '',
    message_count: 0,
  };
  worldStateDisplay: string = '';

  processExchange(state: AgentState): AgentState {
    if (!isValidWorldState(state.worldState)) {
      throw new Error('invalid world state');
    }
    this.worldState = state.worldState;
    this.worldState.message_count = state.messageHistory.length;
    this.worldStateDisplay = JSON.stringify(this.worldState);
    return {messageHistory: state.messageHistory, worldState: this.worldState};
  }
}
