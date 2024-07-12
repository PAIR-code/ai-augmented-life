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

import {NgModule} from '@angular/core';
import {CommonModule, NgComponentOutlet} from '@angular/common';
import {RouterOutlet, RouterModule, Routes} from '@angular/router';

import {BrowserModule} from '@angular/platform-browser';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {HttpClientModule} from '@angular/common/http';

import {AppComponent} from './app.component';
import {SpeechRecognizerComponent} from '@components/speech-recognizer/speech-recognizer.component';
import {AgentSelectorComponent} from '@components/agent-selector/agent-selector.component';

import {MatButtonModule} from '@angular/material/button';
import {MatChipsModule} from '@angular/material/chips';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatIconModule} from '@angular/material/icon';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatCardModule} from '@angular/material/card';
import {MatListModule, MatListItem} from '@angular/material/list';
import {HistoryTutorComponent} from '@components/agents/history-tutor/history-tutor.component';
import {FakeAgentComponent} from '@components/agents/fake-agent/fake-agent.component';

export const routes: Routes = [
  {
    path: '',
    component: AppComponent,
  },
];

const materialModules = [
  MatButtonModule,
  MatChipsModule,
  MatIconModule,
  MatToolbarModule,
  MatSidenavModule,
  MatListModule,
  MatListItem,
  MatCardModule,
];

@NgModule({
  declarations: [
    AppComponent,
    SpeechRecognizerComponent,
    AgentSelectorComponent,
    HistoryTutorComponent,
    FakeAgentComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    CommonModule,
    HttpClientModule,
    NgComponentOutlet,
    RouterModule.forRoot(routes),
    RouterOutlet,
    ...materialModules,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
