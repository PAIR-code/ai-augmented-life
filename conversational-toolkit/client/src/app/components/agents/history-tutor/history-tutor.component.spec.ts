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

import {ComponentFixture, TestBed} from '@angular/core/testing';

import {HistoryTutorComponent, WorldState} from './history-tutor.component';

describe('HistoryTutorComponent', () => {
  let component: HistoryTutorComponent;
  let fixture: ComponentFixture<HistoryTutorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HistoryTutorComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(HistoryTutorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

describe('HistoryTutorComponent', () => {
  let component: HistoryTutorComponent;

  it('should calculate %age questions answered', () => {
    // Zero percent.
    component = new HistoryTutorComponent();
    component.worldState = {
      question: 'What is the capital of France?',
      answers: [
        {answer: 'Paris', hasAnswered: 'false'},
        {answer: 'London', hasAnswered: 'false'},
        {answer: 'Berlin', hasAnswered: 'false'},
      ],
    } as WorldState;

    expect(component.calculatePercentageComplete()).toBe(0);

    // 33 percent.
    component.worldState.answers[0].hasAnswered = 'true';
    expect(component.calculatePercentageComplete()).toBe(33);
  });
});
