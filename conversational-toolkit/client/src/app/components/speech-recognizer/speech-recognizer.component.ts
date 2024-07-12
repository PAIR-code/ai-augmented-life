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

//https://developer.chrome.com/blog/voice-driven-web-apps-introduction-to-the-web-speech-api

import {Component} from '@angular/core';
import {NgZone, Output, EventEmitter} from '@angular/core';
import {environment} from 'environments/environment';

enum ListenState {
  Stopped = 'stopped',
  Listening = 'listening',
  Processing = 'processing',
  Speaking = 'speaking',
  Paused = 'paused',
}

@Component({
  selector: 'app-speech-recognizer',
  templateUrl: './speech-recognizer.component.html',
  styleUrl: './speech-recognizer.component.scss',
})
export class SpeechRecognizerComponent {
  private apiUrl = `${environment.apiUrl}/tts?text=`;
  private recognition: SpeechRecognition | null = null;
  private audio = new Audio();
  private start_timestamp = 0;

  dialogLine: string = '';
  listenState: ListenState = ListenState.Stopped;

  // Spinner displayed when speech recognizer is first started
  // after loading to prevent the user speaking before the
  // recognizer is ready.
  microphoneSpinner = false;
  firstStartAfterPageLoad = true;

  @Output() newDialogLineEvent = new EventEmitter<string>();
  @Output() newInterimDialogLineEvent = new EventEmitter<string>();
  @Output() startListeningEvent = new EventEmitter<void>();

  constructor(private zone: NgZone) {
    if (!('webkitSpeechRecognition' in window)) {
      console.log('webkitSpeechRecognition not found in window');
      return;
    }

    this.recognition = new webkitSpeechRecognition();
    this.recognition.continuous = true;
    this.recognition.interimResults = true;

    // called by speech recognition engine
    this.recognition.onstart = () => {
      console.log('Speech recognition started');
      this.zone.run(() => {
        this.listenState = ListenState.Listening;
      });
    };

    this.recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
      if (event.error === 'no-speech') {
        console.log('info_no_speech');
      }
      if (event.error === 'audio-capture') {
        console.log('info_no_microphone');
      }
      if (event.error === 'not-allowed') {
        if (event.timeStamp - this.start_timestamp < 100) {
          console.log('info_blocked');
        } else {
          console.log('info_denied');
        }
      }
    };

    // called by speech recognition engine
    this.recognition.onend = () => {
      if (this.listenState === ListenState.Listening) {
        // This is a timeout from the speechAPI so automatically restart.
        console.log('SpeechAPI timeout, automatically restarting.');
        this.recognition!.start();
      }
    };

    // called by speech recognition engine
    this.recognition.onresult = (event: SpeechRecognitionEvent) => {
      this.zone.run(() => {
        this.handleSpeechResult(event);
      });
    };
  }

  handleSpeechResult(event: SpeechRecognitionEvent) {
    let interimTranscript = '';
    for (let i = event.resultIndex; i < event.results.length; ++i) {
      // confidence > 0 is required for Android Chrome
      if (event.results[i].isFinal && event.results[i][0].confidence > 0) {
        const line: string = event.results[i][0].transcript;
        if (!line) {
          return;
        }
        this.dialogLine = line;
        // Emit an event to send this line of dialog to the request to the server
        this.listenState = ListenState.Processing;
        this.newDialogLineEvent.emit(this.dialogLine);
      } else {
        interimTranscript += event.results[i][0].transcript;
      }
    }
    if (interimTranscript !== '') {
      this.dialogLine = interimTranscript;
      this.newInterimDialogLineEvent.emit(this.dialogLine);
    }
  }

  isListening() {
    return this.listenState === ListenState.Listening;
  }

  getStatusMessage() {
    switch (this.listenState) {
      case ListenState.Stopped:
        return 'Click the microphone icon to start the conversation...';
      case ListenState.Listening:
        return 'Listening...';
      case ListenState.Processing:
        return 'Processing...';
      case ListenState.Speaking:
        return 'Talking...';
      case ListenState.Paused:
        return 'Click the microphone to continue the conversation...';
    }
  }

  handleAgentResponse(response: string) {
    this.dialogLine = '';
    response = encodeURIComponent(response);
    this.audio.src = this.apiUrl + response;

    // Pause the speech recognition while the audio is playing
    this.zone.run(() => {
      this.listenState = ListenState.Speaking;
      this.recognition!.stop();
    });

    this.audio.load();
    this.audio.play();
    this.audio.onended = () => {
      this.zone.run(() => {
        this.listenState = ListenState.Listening;
        this.recognition!.start();
      });
    };
  }

  // Called by user button press.
  onStartStop() {
    if (this.isListening()) {
      this.listenState = ListenState.Paused;
      this.recognition!.stop();
    } else {
      // If the user starts speaking too soon the speech recognition
      // isn't ready, in the absence of an event from the recognizer
      // this is just a bit of syntactic sugar.
      if (this.firstStartAfterPageLoad) {
        this.firstStartAfterPageLoad = false;
        this.microphoneSpinner = true;
        setTimeout(() => {
          this.microphoneSpinner = false;
        }, 700);
      }

      this.audio.pause(); // Stop the audio from playing
      this.recognition!.lang = 'en-US';
      this.recognition!.start();
      this.startListeningEvent.emit();
      this.listenState = ListenState.Listening;
      this.start_timestamp = Date.now(); // Assign current timestamp
    }
  }
}
