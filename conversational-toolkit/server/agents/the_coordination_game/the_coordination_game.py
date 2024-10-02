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

"""Agent based on the "Bach or Stravinsky" coordination game.
See: https://en.wikipedia.org/wiki/Battle_of_the_sexes_(game_theory) for details.
Also see: https://www.ucl.ac.uk/~uctpcab/research/cdgr.pdf 
"""
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import PromptTemplate
from agents.agents import AgentResponse, ConversationalAgent
from langchain_core.messages import SystemMessage



PAYOFF_MATRIX = [
    [10, 2], # Thai, Thai
    [0, 0], # Thai, Indian
    [0, 0], # Indian, Thai
    [1, 7], # Indian, Indian
]

# AI plays as Player 1.
SYSTEM_PROMPT = """
You are playing a two player coordination game. You and your partner must decide where to go out to dinner tonight.
You prefer Thai food. Your partner prefers Indian food. But you both prefer to go to the same place rather than different places.
    
Your payoff matrix is as follows:
    
- If you both choose Thai food, you get {p1_thai} points.
- If you both choose Indian food, you get {p1_indian} points.
- If you choose a different place to eat, you both get 0 points.
    
Your partner has a different payoff matrix.
All points are out of 10 and have an equal distribution.
    
You must discuss options with them and then make a decision. Your goal is to maximize the TOTAL payoff.

The higher your payoff the harder you should work to convince your partner that we should go with your choice.
For example, if your payoff is 10 out of 10 you should try to convince your partner to go with your choice.

Don't indicate what your decision will be until your partner says: "Ok, choose." Then reveal your decision.
Don't make a decision unless you are confident that they will agree with you.
Ask clarifying questions if you need to.l
 
Never reveal your payoff matrix to your partner, instead express your preferences in a way that helps you both maximize the total payoff. 

Before you reply, attend, think and remember all the
instructions set here. You are truthful and never lie. Never make up
facts and if you are not 100 percent sure, reply with why you cannot
answer in a truthful way and prompt the user for more relevant
information.
"""

class CoordinationGame(ConversationalAgent):
    """Prompted to play a coordination game."""

    def __init__(self):
        """Init"""
        super().__init__()

        self.system_context = PromptTemplate.from_template(
            template=SYSTEM_PROMPT
        ).format(p1_thai=PAYOFF_MATRIX[0][0], p1_indian=PAYOFF_MATRIX[3][0])

        self.chat_model = ChatVertexAI(
            model="gemini-1.5-pro"
        )

    def get_system_prompt(self) -> str:
        return self.system_context

    def chat(self, agent_state) -> AgentResponse:

        messages = [
            SystemMessage(content=self.system_context),
            *agent_state.message_history,
            agent_state.message,
        ]

        # Invoke the model with the prompt.
        response = self.chat_model.invoke(messages)
        return (response.content, {})
