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
# pylint: disable=missing-module-docstring, missing-function-docstring, missing-class-docstring, line-too-long, protected-access

import json
import unittest

from langchain_google_vertexai import VertexAI
from utils.test_utils import evaluate, send_chat

from ..agents import AgentState
from .history_tutor import (
    HistoryTutor,
    load_file,
    BLACK_DEATH_TUTOR_CONTEXT,
)


class TestHistoryTutor(unittest.TestCase):

    def setUp(self):
        self.llm = VertexAI(model_name="gemini-1.5-pro")
        self.tutor = HistoryTutor()

    def test_loads_initial_world_state(self):
        lesson = self.tutor._lesson_context
        self.assertIsNotNone(lesson["question"])
        self.assertEqual(len(lesson["answers"]), 4)

    def test_introduce_lesson_and_ask_first_question(self):
        transcript = ["start lesson"]

        response, _ = self.tutor.chat(AgentState("start lesson", [], None))

        success = evaluate(
            transcript,
            response,
            guidance="Does the output provide a short introduction to the subject of the Black Death and ask a first question on a topic related to the Black Death?",
            examples=[
                "Let's begin our lesson on the Black Death. What were the different theories about the cause of the Black Death?"
            ],
            verbose=False,
        )

        self.assertTrue(
            success, f"Evaluation of model response failed. Response was: {response}"
        )

    def test_student_gives_two_answers_correctly(self):
        world_state = json.loads(load_file(BLACK_DEATH_TUTOR_CONTEXT))
        transcript = [
            "start lesson",
            "Let's begin our lesson on the Black Death. What were the different theories about the cause of the Black Death?",
            "The four humors and the miasma theory.",
        ]

        response, world_state = send_chat(self.tutor, transcript, world_state)

        # Four humours and miasma have both been marked as true.
        self.assertEqual(world_state["answers"][1]["hasAnswered"], "true", world_state)
        self.assertEqual(world_state["answers"][2]["hasAnswered"], "true", world_state)

        success = evaluate(
            transcript,
            response,
            guidance="""Does the output congratulate the student. Then, does it ask the student to provide more answers to the current question?""",
            examples=[
                "Great! You're correct. The four humors and the miasma theory were two theories about the cause of the Black Death. Can you think of any others?"
            ],
            verbose=False,
        )

        self.assertTrue(
            success,
            f"Evaluation of model response failed. Response was: {response}.",
        )

    def test_update_world_state_no_answers(self):
        world_state = json.loads(load_file(BLACK_DEATH_TUTOR_CONTEXT))
        last_answer = "start lesson."
        world_state = self.tutor._update_question_state(world_state, last_answer)
        self.assertEqual("false", world_state["answers"][0]["hasAnswered"])
        self.assertEqual("false", world_state["answers"][1]["hasAnswered"])
        self.assertEqual("false", world_state["answers"][2]["hasAnswered"])
        self.assertEqual("false", world_state["answers"][3]["hasAnswered"])

    def test_update_world_state_two_answers(self):
        world_state = json.loads(load_file(BLACK_DEATH_TUTOR_CONTEXT))
        last_answer = "The four humors and the miasma theory."
        world_state = self.tutor._update_question_state(world_state, last_answer)
        self.assertEqual(world_state["answers"][1]["hasAnswered"], "true")
        self.assertEqual(world_state["answers"][2]["hasAnswered"], "true")

    def test_update_world_state_all_answers(self):
        world_state = json.loads(load_file(BLACK_DEATH_TUTOR_CONTEXT))
        last_answer = "Punishment from God, the four humors theory, miasma theory, and strangers or outsiders."
        world_state = self.tutor._update_question_state(world_state, last_answer)
        self.assertEqual(world_state["answers"][0]["hasAnswered"], "true")
        self.assertEqual(world_state["answers"][1]["hasAnswered"], "true")
        self.assertEqual(world_state["answers"][2]["hasAnswered"], "true")
        self.assertEqual(world_state["answers"][3]["hasAnswered"], "true")


if __name__ == "__main__":
    unittest.main()
