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

import {Component, ElementRef, inject, OnInit, ViewChild} from '@angular/core';
import {NgComponentOutlet} from '@angular/common';
import {SpeechRecognizerComponent} from '@components/speech-recognizer/speech-recognizer.component';
import {AgentSelectorComponent} from '@components/agent-selector/agent-selector.component';
import {ChatService} from '@services/chat.service';
import {AgentsService, AgentComponentConfig} from '@services/agents.service';
import {ChatMessage, AgentId, AgentState, AGENT_IDS} from '@data/agent';
import {debounce} from './util/debounce';
import {ActivatedRoute} from '@angular/router';
import {Location} from '@angular/common';
import {Inject} from '@angular/core';
import {DOCUMENT} from '@angular/common';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent implements OnInit {
  @ViewChild(SpeechRecognizerComponent)
  speechRecognizerComponent!: SpeechRecognizerComponent;
  @ViewChild(AgentSelectorComponent)
  agentSelectorComponent!: AgentSelectorComponent;
  @ViewChild('content', {read: ElementRef})
  contentElement!: ElementRef;
  @ViewChild(NgComponentOutlet, {static: false})
  agentComponentOutlet!: NgComponentOutlet;

  conversation: ChatMessage[] = [];
  interimDialogLine: string = '';

  agentId: AgentId = 'default';
  currentAgentConfig: AgentComponentConfig;
  private agentState: AgentState = {messageHistory: [], worldState: null};
  private readonly agentConfigs = inject(AgentsService).getAgentConfigs();

  private debouncedScrollToBottom: () => void;

  constructor(
    private chatService: ChatService,
    private route: ActivatedRoute,
    private location: Location,
    @Inject(DOCUMENT) private document: Document
  ) {
    this.currentAgentConfig = this.agentConfigs.get(this.agentId)!;
    this.debouncedScrollToBottom = debounce(this.scrollToBottom);
  }

  ngOnInit() {
    this.route.queryParamMap.subscribe(params => {
      const agentIdParam = params.get('agent');
      if (AGENT_IDS.includes(agentIdParam as AgentId)) {
        this.handleAgentIdChange(agentIdParam as AgentId);
      }
    });
  }

  enterFullscreenModeOnMobile() {
    if (
      this.document.fullscreenEnabled &&
      /Mobi|Android/i.test(navigator.userAgent)
    ) {
      this.document.documentElement.requestFullscreen();
    }
  }

  handleStartListening() {
    this.enterFullscreenModeOnMobile();
  }

  handleAgentIdChange(agentId: AgentId) {
    this.agentId = agentId;
    this.currentAgentConfig = this.agentConfigs.get(this.agentId)!;

    // Update browser location bar to add ?agent=[agentId]
    this.location.replaceState(`?agent=${this.agentId}`);

    // Clear conversation & world state when changing agents.
    this.conversation = [];
    this.agentState = {messageHistory: [], worldState: null};
  }

  handleNewLineOfDialog(dialog: string) {
    if (!dialog) {
      return;
    }
    const responseObservable = this.chatService.sendMessage(
      dialog,
      this.conversation,
      this.agentState.worldState as object,
      this.agentId
    );
    responseObservable.subscribe((agentResponse: string) => {
      // Update the UI only once, when we receive the LLM response.
      this.interimDialogLine = '';

      const parsedResponse = JSON.parse(agentResponse);
      const agentDialog = parsedResponse['response'];
      const worldState = parsedResponse['world_state'];
      const userMessage = {content: dialog, author: 'human' as const};
      const agentMessage = {content: agentDialog, author: 'ai' as const};
      this.conversation = [...this.conversation, userMessage, agentMessage];
      this.speechRecognizerComponent.handleAgentResponse(agentDialog);

      const agentState = {messageHistory: this.conversation, worldState};
      const agent = this.agentComponentOutlet['_componentRef'].instance;
      if (agent) {
        this.agentState = agent.processExchange(agentState);
      }

      if (!this.currentAgentConfig.preferences.shouldHideChat) {
        this.debouncedScrollToBottom();
      }
    });
  }

  handleNewInterimDialogLineEvent(dialog: string) {
    this.interimDialogLine = dialog;
  }

  donwloadTranscript() {
    this.chatService.downloadTranscript(this.conversation);
  }

  private scrollToBottom() {
    this.contentElement.nativeElement.scroll({
      top: this.contentElement.nativeElement.scrollHeight,
      left: 0,
      behavior: 'smooth',
    });
  }
}
