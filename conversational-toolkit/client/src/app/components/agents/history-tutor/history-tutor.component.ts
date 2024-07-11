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

export interface WorldState {
  question: string;
  answers: Answer[];
}

interface Answer {
  answer: string;
  hasAnswered: string;
}

@Component({
  selector: 'app-history-tutor',
  templateUrl: './history-tutor.component.html',
  styleUrl: './history-tutor.component.css',
})
export class HistoryTutorComponent implements Agent {
  worldState: WorldState | null = null;

  // Called when server responds with a new state and chat response.
  processExchange(state: AgentState) {
    console.log(state.worldState);

    this.worldState = state.worldState as WorldState;
    return {...state, worldState: this.worldState};
  }

  calculatePercentageComplete() {
    let correctAnswers = 0;
    let totalAnswers = 0;

    if (this.worldState == undefined) {
      return 0;
    }

    for (const answer of this.worldState.answers) {
      totalAnswers += 1;
      if (answer.hasAnswered === 'true') {
        correctAnswers += 1;
      }
    }
    if (totalAnswers == 0) {
      return 0;
    }
    return Math.round((correctAnswers / totalAnswers) * 100);
  }
}
