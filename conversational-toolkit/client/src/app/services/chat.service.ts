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

import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {ChatMessage, AgentId} from '@data/agent';
import {environment} from 'environments/environment';

@Injectable({
  providedIn: 'root',
})
export class ChatService {
  private apiUrl = `${environment.apiUrl}/chat`;

  constructor(private http: HttpClient) {}

  sendMessage(
    request: string,
    messageHistory: ChatMessage[],
    worldState: unknown,
    agentId: AgentId
  ): Observable<string> {
    const formData = new FormData();
    formData.append('q', request);
    formData.append('message_history', JSON.stringify(messageHistory));
    formData.append('world_state', JSON.stringify(worldState));
    formData.append('agent_id', agentId);
    return this.http.post(this.apiUrl, formData, {responseType: 'text'});
  }

  downloadTranscript(messageHistory: ChatMessage[]) {
    const transcript = messageHistory
      .map(msg => `<${msg.author}>${msg.content}</${msg.author}>`)
      .join('\n\n');
    const filename = `chat_transcript-${Date.now()}.txt`;
    this.downloadFile(transcript, filename, 'text/plain');
  }

  private downloadFile(data: string, filename: string, type: string) {
    const blob = new Blob([data], {type: type});
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click(); // Trigger the download
    window.URL.revokeObjectURL(url); // Clean up
  }
}
