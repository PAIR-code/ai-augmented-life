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

import {Component, EventEmitter, inject, Input, Output} from '@angular/core';
import {AgentId} from '@data/agent';
import {AgentsService} from '@services/agents.service';

@Component({
  selector: 'app-agent-selector',
  templateUrl: './agent-selector.component.html',
  styleUrl: './agent-selector.component.css',
})
export class AgentSelectorComponent {
  private readonly agentConfigs = inject(AgentsService).getAgentConfigs();

  @Input() selectedAgentId: AgentId | null = null;

  @Output() selectedAgentIdChange = new EventEmitter<AgentId>();

  get _agentIds() {
    return [...this.agentConfigs.keys()];
  }

  agentSelectionChanged(agentId: AgentId) {
    this.selectedAgentId = agentId;
    this.selectedAgentIdChange.emit(agentId);
  }

  getAgentDisplayName(agentId: AgentId) {
    const config = this.agentConfigs.get(agentId)!;
    return config.preferences.displayName;
  }
}
