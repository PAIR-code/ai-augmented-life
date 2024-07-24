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

import {Component, Injectable} from '@angular/core';
import {Agent, AgentId} from '@data/agent';

import {HistoryTutorComponent} from '@components/agents/history-tutor/history-tutor.component';
import {FakeAgentComponent} from '@components/agents/fake-agent/fake-agent.component';
import {DefaultAgentComponent} from '@components/agents/default-agent/default-agent.component';
import {PhysicsExpertComponent} from '@components/agents/physics-expert/physics-expert.component';
import {EmpathaiComponent} from '@components/agents/empathai/empathai.component';

export interface AgentComponentConstructor {
  new (): Agent & Component;
}

export interface AgentComponentPreferences {
  // Required preferences for all agents.
  readonly displayName: string;
  // Optional preferences default to false
  readonly shouldHideChat?: boolean;
  readonly shouldTruncateChatHistory?: boolean;
}

export interface AgentComponentConfig {
  component: AgentComponentConstructor;
  inputs: Record<string, unknown>;
  preferences: AgentComponentPreferences;
}

@Injectable({
  providedIn: 'root',
})
export class AgentsService {
  // Returns an agent component repository keyed by agent id.
  // New agents should be registered here.
  getAgentConfigs(): Map<AgentId, AgentComponentConfig> {
    return new Map<AgentId, AgentComponentConfig>([
      [
        'default',
        {
          component: DefaultAgentComponent,
          inputs: {
            model: 'Gemini',
          },
          preferences: {
            displayName: 'Default Agent',
          },
        },
      ],
      [
        'fake',
        {
          component: FakeAgentComponent,
          inputs: {},
          preferences: {
            displayName: 'Fake Agent',
          },
        },
      ],
      [
        'history_tutor',
        {
          component: HistoryTutorComponent,
          inputs: {},
          preferences: {
            displayName: 'History Tutor',
            shouldTruncateChatHistory: true,
          },
        },
      ],
      [
        'physics_expert',
        {
          component: PhysicsExpertComponent,
          inputs: {},
          preferences: {
            displayName: 'Physics Expert',
          },
        },
      ],
      [
        'empathai',
        {
          component: EmpathaiComponent,
          inputs: {},
          preferences: {
            displayName: 'empath.ai',
            shouldTruncateChatHistory: true,
            shouldHideChat: true,
          },
        },
      ],
    ]);
  }
}
