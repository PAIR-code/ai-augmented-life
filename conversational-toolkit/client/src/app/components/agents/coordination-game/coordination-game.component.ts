import {Component} from '@angular/core';
import {Agent, AgentState} from '@data/agent';

@Component({
  selector: 'app-coordination-game',
  standalone: true,
  imports: [],
  templateUrl: './coordination-game.component.html',
  styleUrl: './coordination-game.component.css',
})
export class CoordinationGameComponent implements Agent {
  PAYOFF_MATRIX = [
    [3, 2], // Thai, Thai
    [0, 0], // Thai, Indian
    [0, 0], // Indian, Thai
    [1, 7], // Indian, Indian
  ];

  p2_indian = this.PAYOFF_MATRIX[3][1];
  p2_thai = this.PAYOFF_MATRIX[0][1];

  processExchange(state: AgentState): AgentState {
    return state;
  }
}
