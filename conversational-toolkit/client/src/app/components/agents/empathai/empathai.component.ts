import {Component} from '@angular/core';
import {Agent, AgentState} from '@data/agent';

export class MarkingRubric {
  clarifiesExistingKnowledge: number = 0;
  introducesPurposeOfConversation: number = 0;
  usesWarningShot: number = 0;
  explainsWhatHasHappened: number = 0;
  deliversInformationInSmallChunks: number = 0;
  checksUnderstanding: number = 0;
  allowsTimeAndSpaceToAnswerQuestions: number = 0;
  remainsCalmEmpathicNonJudgemental: number = 0;
  demonstratesActiveListeningFollowsCues: number = 0;
  summarisesConversationAndAgreedNextSteps: number = 0;
}

@Component({
  selector: 'app-empathai',
  standalone: true,
  imports: [],
  templateUrl: './empathai.component.html',
  styleUrl: './empathai.component.css',
})
export class EmpathaiComponent implements Agent {
  markingRubric: MarkingRubric = new MarkingRubric();

  processExchange(state: AgentState): AgentState {
    this.markingRubric = state.worldState as MarkingRubric;
    return {...state, worldState: this.markingRubric};
  }
}
