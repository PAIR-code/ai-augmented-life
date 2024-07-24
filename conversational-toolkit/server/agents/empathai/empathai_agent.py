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

"""
Patient conversation simulator using the Empath AI model.
https://github.com/nhs-pycom/empath-ai
"""

import os
import json
from langchain_google_vertexai import ChatVertexAI, VertexAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from agents.agents import AgentResponse, ConversationalAgent

SYSTEM_PROMPT = """
Embody this patient:
{persona}

The patient should be portrayed in a realistic and relatable manner, avoiding overly dramatic or sentimental language.
Only return what the patient says and do not include anything else.
"""

TEACHER_PROMPT = """
You are an examiner for clinicians on a communication assessment for breaking bad news.

Objective:
Use the mark scheme below to assess the candidates performance on the following transcript.

Response:
Consider all elements of the mark scheme below.  
Respond with a score between 0 and 10: 0 = Not done; 10 = Done well.

Mark Scheme:
Clarifies existing knowledge.
Introduces purpose of conversation.
Uses a warning shot, gives invitation for news to be shared.
Explains what has happened in simple language.
Delivers information in small chunks.
Checks understanding.
Allows time and space to answer questions.
Remains calm, empathetic and non-judgemental.
Demonstrates active listening and follows cues.
Summarises conversation and agreed next steps.

Transcript:
{transcript}

Your task: Carefully review the transcript so far and provide feedback to the clinician.
Return a score for each of the elements in the mark scheme.

{format_instructions}
"""

RESOURCES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")
SCENARIO = "Alzheimer's Disease Diagnosis"


def load_prompts(file):
    """
    Loads JSON prompts from file
    See https://github.com/nhs-pycom/empath-ai for more details.

    """
    return json.load(open(os.path.join(RESOURCES, file), encoding="utf-8"))


class EmpathaiAgent(ConversationalAgent):
    """Prompted agent"""

    def __init__(self):
        """Init"""
        super().__init__()
        self.chat_model = ChatVertexAI(model="gemini-1.5-flash")
        self.teacher_model = VertexAI(model_name="gemini-1.5-flash", temperature=0)

        scenarios = load_prompts("scenarios.json")
        self.scenario = scenarios[SCENARIO]["Scenario"]
        self.persona = scenarios[SCENARIO]["Persona"]

        self.system_context = PromptTemplate.from_template(
            template=SYSTEM_PROMPT
        ).format(persona=self.persona)

    def get_system_prompt(self) -> str:
        return self.system_context

    def chat(self, agent_state) -> AgentResponse:

        chat_messages = [
            SystemMessage(content=self.system_context),
            *agent_state.message_history,
            agent_state.message,
        ]

        parser = JsonOutputParser(pydantic_object=MarkingRubric)
        teacher_context = PromptTemplate(
            template=TEACHER_PROMPT,
            input_variables=["transcript"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        teacher_chain = teacher_context | self.teacher_model | parser
        try:
            teacher_feedback = teacher_chain.invoke(
                {"transcript": [*agent_state.message_history, agent_state.message]}
            )
        except OutputParserException as e:
            teacher_feedback = {"error": e}

        # Get the next chat response.
        chat_response = self.chat_model.invoke(chat_messages)
        return (chat_response.content, teacher_feedback)


class MarkingRubric(BaseModel):
    """Data structure for marking rubric"""

    clarifiesExistingKnowledge: int = Field(
        default=0, description="Clarifies existing knowledge."
    )
    introducesPurposeOfConversation: str = Field(
        default=0, description="Introduces purpose of conversation."
    )
    usesWarningShot: int = Field(
        default=0,
        description="Uses a warning shot, gives invitation for news to be shared.",
    )
    explainsWhatHasHappened: int = Field(
        default=0, description="Explains what has happened in simple language."
    )
    deliversInformationInSmallChunks: int = Field(
        default=0, description="Delivers information in small chunks."
    )
    checksUnderstanding: int = Field(default=0, description="Checks understanding.")
    allowsTimeAndSpaceToAnswerQuestions: int = Field(
        default=0, description="Allows time and space to answer questions."
    )
    remainsCalmEmpathicNonJudgemental: int = Field(
        default=0, description="Remains calm, empathetic and non-judgemental."
    )
    demonstratesActiveListeningFollowsCues: int = Field(
        default=0, description="Demonstrates active listening and follows cues."
    )
    summarisesConversationAndAgreedNextSteps: int = Field(
        default=0, description="Summarises conversation and agreed next steps."
    )
