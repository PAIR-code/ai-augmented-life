# Copyright 2024 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utility functions used by unit tests."""

from typing import List
from langchain_google_vertexai import VertexAI
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage
from langchain_core.prompts import PromptTemplate

from agents.agents import AgentState


def build_message_history_for_test(message_history: List[str]) -> list[BaseMessage]:
    """Takes a list of strings and returns a list of BaseMessage objects suitable
    for ChatPromptTemplate.from_messages.

    Args:
        message_history: list of strings. Assumes alternating Human/AI messages starting with
        a human message. Required an even number of messages in order to finish with the last AI
        response.

    Returns:
        list[langchain.BaseMessage]: Alternating list of AIMessage and HumanMessage objects or
        an empty list.

    Raises:
        ValueError: If there are an even number of messages.
    """
    rtn = []
    if not message_history:
        return rtn

    for i, message in enumerate(message_history):
        if i % 2 == 0:
            rtn.append(HumanMessage(message))
        else:
            rtn.append(AIMessage(message))
    return rtn


def send_chat(agent, transcript, world_state):
    """
    Send a chat message to the agent and return the response and world state.

    Args:
        agent: Agent object to chat with.
        transcript: List of strings representing the conversation history.
            Assumes alternating Human/AI messages starting with a human
            message. Must be an odd number of messages in order to finish
            with a human message.
        world_state: Dictionary representing the world state.

    Returns:
        Tuple of the agent response and the world state.

    Raises:
        ValueError: If the transcript doesn't follow the expected format.
    """
    message_history = build_message_history_for_test(transcript[0:-1])
    latest_message = transcript[-1]
    return agent.chat(AgentState(latest_message, message_history, world_state))


EVALUATION_PROMPT = """
You are now in evaluation mode. Consider the following conversation history in order to evaluate how accurately the model responded to the last message.

Transcript: 
{transcript}

The AI response:
AI: {response}

Based on the following criteria: {criteria}.

Think step by step and decide if the model's response was correct.

1. Does the model response conform to the requirements described in the criteria?
2. Is the model response similar to the examples below. 

Examples of valid responses:
{examples}

If EITHER of these conditions are met, respond with 'Y'. Otherwise, respond with 'N'.

Now provide your evaluation with a single character response:
Y - Yes, the model met the criteria or returned a response similar to one of the references.
N - No, the model did not meet the criteria or returned a response that was not similar to any of the references.

Don't return any text other than for Y or N.
"""

MAX_RETRIES = 3


def evaluate(transcript, response, guidance, examples=None, verbose=False):
    """Helper function to evaluate a model response based on a examples and evaluation criteria."""
    prompt = PromptTemplate.from_template(EVALUATION_PROMPT)

    transcript_text = "\n".join(
        [
            f"Human: {message}" if i % 2 == 0 else f"AI: {message}"
            for i, message in enumerate(transcript)
        ]
    )

    llm = VertexAI(model_name="gemini-1.5-flash", temperature=0.0)
    prompt_text = prompt.format(
        transcript=transcript_text,
        response=response,
        criteria=guidance,
        examples="\n".join(examples),
    )

    if verbose:
        print(f"\n -- Evaluation Prompt --\n {prompt_text} \n---\n")

    retry_count = 0
    final_evaluation = None
    while retry_count < MAX_RETRIES:

        resp = llm.invoke(prompt_text)
        text = resp.strip()

        if verbose:
            print(f"Model response: {text}")

        if text not in ["Y", "N"]:
            retry_count += 1
        else:
            final_evaluation = text
            break

    if final_evaluation is None:
        raise ValueError("Failed to parse the model response after 3 retries.")

    return final_evaluation == "Y"
