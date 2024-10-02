# Testing and Developing Agents
If you follow the [Getting Started](./docs/getting-started.md) steps you should have a new custom AI voice assistant. The next step is to iterate on the prompt to refine your assistant's performance.

A simple tool is provided to make that process more convenient:

## Chat Client
The first step is to give it a try with the voice interface. But iterating via voice can be time consuming. To streamline things we built ```scripts/chat_client.py``` — a simple script that allows you to interact with an agent via the command line:

```sh
cd server
python3 -m scripts.chat_client --agent physics_expert
```

We added a handful of commands to the chat client that can be used to debug the agent in-situ.

* ```/clear``` - clear the conversation history and world state and start a fresh conversation
* ```/undo``` - remove the last exchange in the conversation history. This makes it possible to 'rewind' the conversation to try different conversation paths, phrases, or updated prompts
* ```/transcript``` - dumps a transcript of the conversation so far
* ```/worldstate``` - shows the hidden state that can be used to help the language model keep track of the current point in the conversatino (for example, in the history tutor example we keep track of what questions the student has correctly answered)
* ```/feedback``` - provide feedback to the agent or list feedback so far (see below for a discussion of the feedback process)
* ```/principles``` - principles will use the [Model Alignment](https://github.com/PAIR-code/model-alignment) library to generate principles based on your feedback so far, which can be inserted into the prompt
* ```/exit``` - end the conversation

For convenience, the client auto-reloads whenever the prompt is changed. Used in conjunction with ```/undo``` this provides a convenient way to iteratively explore possible conversation paths and adjust the prompt to amplify or suppress specific behaviours.
