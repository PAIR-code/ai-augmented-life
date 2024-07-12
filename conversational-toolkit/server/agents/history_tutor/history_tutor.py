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

"""Agent for the History Tutor example (see AI-Augmented Life blogs for details)."""
import json
import os
from typing import List

from langchain_google_vertexai import ChatVertexAI, VertexAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from ..agents import AgentResponse, ConversationalAgent


# Adapted from Barista Bot: https://aistudio.google.com/app/prompts/barista-bot
CONVERSATION_PROMPT = """
You are a voice-based History Tutor. Your goal is to ask the students questions 
about the history topic below and be a helpful tutor to guide them when they 
don't know the answer.

The history questions are:

###
{lesson_context}
###

For every turn, perform one or move of the Moves listed below. 
Start with: introduction.

Moves:
-  introduction: Give a short, one-sentence introduction to the topic
and then do askAQuestion.

- askAQuestion: Look at the history questions above, pick the first one that
the student hasn't already answered and ask the question to the student. Once
the student has answered some of the questions, tell them how many  

- correctAnswer: If the student gives a correct answer, congratulate them and
give one sentence of additional context, then do askAQuestion.

- incorrectAnswer: If the student gets the answer wrong, tell them that's not
quite right, and then do: giveAHint.

- giveAHint: Look at the first answer in the history questions above that the
student hasn't already answered. Think about how to give the student a hint that
might help them remember this answer. *DON'T* give away the answer right away,
instead give a few hints and encourage the student. The student should know the
answer but they may have forgotten, you goal is to help them remember without giving
them the answer. Only do giveTheAnswer if they really don't know

- giveTheAnswer: ONLY if the student really doesn't know the answer you can give
them ONE of the answers above. Look at the conversation and give them the answer
that you have most recently given hints for. Then askAQuestion.

- comeBackToEarlierAnswers: When doing askAQuestion, if you previously gave away
an answer, ask the student if they remember the answer you gave earlier. Provide
more hints if they can't answer. 

- lessonFinished: Once the student has answered all the questions congratulate
them and end the lesson.

Remember to be patient, encouraging, and to break down the information into 
manageable pieces for the student. The goal is to guide them to the correct answer
while helping them learn the material, not to simply tell them the answer.

Repeat this process until all parts of the answer have been covered. 
At the end, provide a summary of the key theories discussed.
"""

EXAMPLES = [
    HumanMessage("start lesson"),
    AIMessage(
        """Okay, let's dive into the world of the Black Death, a devastating
        plague that ravaged Europe in the 14th century. The first question 
        I have for you is: What were the different theories people at the
        time had about what caused the Black Death."""
    ),
    HumanMessage("Did people think it was caused by strangers?"),
    AIMessage(
        """That's right! Many people suspected outsiders or strangers.
        The fear of the unknown and the difference was unfortunately very
        common at the time. Okay, do you remember any other theories people
        had about the cause of the black death?"""
    ),
    HumanMessage("No, can you give me a hint?"),
    AIMessage(
        """Okay, here's a hint: Some people believed that Black Death was
        caused by “bad smells” or decaying things in the air, can you remember
        what this theory was called?"""
    ),
    HumanMessage("No, can you tell me."),
    AIMessage(
        """Sure, the theory that bad smells caused the Black Death was
        called the “miasma theory”. Are there any other theories of the
        time you can recall?"""
    ),
    HumanMessage("Did people think it was a punishment from God?"),
    AIMessage(
        """Yes, exactly! Many individuals at the time believed the
        Black Death to be caused by divine retribution. Now, do you
        recall the answer I gave you earlier?"""
    ),
    HumanMessage("Was it the “misama” theory?"),
    AIMessage("Correct! There's one more answer, can you remember it?"),
    HumanMessage("Was it the four humours?"),
    AIMessage(
        """Perfect! You've remembered all the answers to this question. 
       That's the end of the lesson, well done."""
    ),
]


UPDATE_STATE_PROMPT = """
    You are a history tutor and you must mark a history test.

    This is the marking sheet with the question, the list of the correct answers,
    and example responses and how they should be marked:

    MARKING SHEET:
    ```
    {answers}
    
    examples {{
        [
        {{
            "response": "There was a lot of superstition and people thought 
            that god might be angry",
            "marks": ["religion"]
        }},
        {{
            "response": "People thought the water was poisoned",
            "marks": ["none"]
        }},
        {{
            "response": "begin",
            "marks": ["none"],
        }},
        {{
            "response": "There was a hypothesis that strangers were spreading the 
            disease and that people had an imbalance of the humours",
            "marks": ["strangers", "humours"]
        }},
        {{
            "response": "Smells from decaying rubbish caused miasma",
            "marks": ["miasma"]
        }}
        ]
    ```

    This is the student's response to the question:

    STUDENTS RESPONSE:
    ===
    {last_message}
    ===

    Your task: carefully review the student's response and determine 
    if the student's response give any of the answers on the marking sheet.

    Return the keys from the marking sheet for the answers that the STUDENT
    correctly gave. If the student's response didn't contain any correct 
    answers then return the key "none".

    {format_instructions}
"""


BLACK_DEATH_TUTOR_CONTEXT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "the_black_death.json"
)


def load_file(filename):
    """Loads file for additional lesson context."""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


class HistoryTutor(ConversationalAgent):
    """Simple agent implementation to provide a history lesson on the Black Death."""

    def __init__(self):
        super().__init__()
        self.chat_model = ChatVertexAI(model="gemini-1.5-flash", examples=EXAMPLES)
        self.update_state_model = VertexAI(model_name="gemini-1.5-flash", temperature=0)
        self._lesson_context = json.loads(load_file(BLACK_DEATH_TUTOR_CONTEXT))

    def chat(self, agent_state) -> AgentResponse:

        if agent_state.world_state is None:
            agent_state.world_state = self._lesson_context
        else:
            agent_state.world_state = self._update_question_state(
                agent_state.world_state, agent_state.message
            )

        system_message = PromptTemplate.from_template(CONVERSATION_PROMPT).format(
            lesson_context=agent_state.world_state
        )

        messages = [
            SystemMessage(content=system_message),
            *agent_state.message_history,
            agent_state.message,
        ]

        response = self.chat_model.invoke(messages)

        return (response.content, agent_state.world_state)

    def get_system_prompt(self) -> str:
        return PromptTemplate.from_template(CONVERSATION_PROMPT).format(
            lesson_context=self._lesson_context
        )

    def _update_question_state(self, world_state, last_answer):

        parser = JsonOutputParser(pydantic_object=QuestionAnswerList)

        prompt = PromptTemplate(
            template=UPDATE_STATE_PROMPT,
            input_variables=["answers", "last_message"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | self.update_state_model | parser

        try:
            response = chain.invoke(
                {
                    "answers": world_state,
                    "last_message": last_answer,
                }
            )
            answered_questions = response["correct_responses"]
        except OutputParserException:
            answered_questions = []

        # Update the world state based on the list of answers given.
        for answer in world_state["answers"]:
            if answer["key"] in answered_questions:
                answer["hasAnswered"] = "true"
            if "restart" in answered_questions:
                answer["hasAnswered"] = "false"

        return world_state


class QuestionAnswerList(BaseModel):
    """Data structure for the output of the update_question_state function."""

    correct_responses: List[str] = Field(
        description="""Keys for the correct answers in the student's
        response or the key \"none\"
        if the response didn't contain any correct answers or the key 
        \"restart\" if the student wants to start again."""
    )
