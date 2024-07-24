import {ComponentFixture, TestBed} from '@angular/core/testing';

import {EmpathaiComponent} from './empathai.component';

describe('EmpathaiComponent', () => {
  let component: EmpathaiComponent;
  let fixture: ComponentFixture<EmpathaiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EmpathaiComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(EmpathaiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

describe('EmpathaiComponent', () => {
  let component: EmpathaiComponent;

  it('parses marking rubric', () => {
    component = new EmpathaiComponent();
    const incomingState = {
      clarifies_existing_knowledge: 1,
      introduces_purpose_of_conversation: 0,
      uses_warning_shot: 1,
      explains_what_has_happened: 1,
      delivers_information_in_small_chunks: 1,
      checks_understanding: 1,
      allows_time_and_space_to_answer_questions: 1,
      remains_calm_empathic_non_judgemental: 1,
      demonstrates_active_listening_follows_cues: 1,
      summarises_conversation_and_agreed_next_steps: 1,
    };

    const agentState = {messageHistory: [], worldState: incomingState};

    component.processExchange(agentState);
    expect(component.markingRubric).toEqual(incomingState);
  });
});
