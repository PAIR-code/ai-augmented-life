# Adding A New Agent
Conversational Toolkit is designed to make it simple to experiment with custom prompts, chains, and integrations in order to create custom voice assistants for specific use-cases.

"Agents" are the abstraction used to mediate user/AI interactions and they are implemented as follows:

1. A python class on the server that communicates with an LLM (e.g. prompt-chain + supplementary RAG, integrations, world state).

2. An Angular component on the client with optional custom UI.

To create a new agent you will need to add server and client implementations.

## Server

* Define a new python module that subclasses the `ConversationalAgent` and implements the `chat` method. Use ```server/agents/default_agent.py``` as an example.

* Add a reference to the new agent with a unique id to `_AGENT_BY_ID` in `server/agents/registry.py`.

## Client

* Create an Angular component:
```sh
cd client
npm run ng g component components/agents/your-agent-name
```

* Implement the `Agent` interface (`app/data/agent.ts`) in your component's class (`components/agents/your-agent-name.ts`).

A minimal implementation would just return the `state` object unchanged. Use the `default_agent` component for reference. For example:

```ts
export class YourAgentComponent implements Agent {
  processExchange(state: AgentState): AgentState {
    return state; 
  }
}
```

* Add a unique identifier for your agent to `AGENT_IDS` in `app/data/agent.ts`.
* Register your agent component and its preferences in `app/services/agents.service.ts`.

After these steps, you should see your agent's name in the app's side bar and selecting it should display its component UI. Talking via the Web application with this agent selected should route calls to the appropriate python file.

See [Testing and Developing Agents](./docs/testing-and-developing.md) for more discussion on how to iterate on conversation agents.
