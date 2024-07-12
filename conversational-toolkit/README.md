# Conversational Toolkit

The Conversational Toolkit is a Web application that provides a simple prototyping environment for voice-driven conversational AI agents.

The toolkit fronts a language model with automatic speech recognition (ASR) using the WebSpeech API, and text-to-speech (TTS) using the Vertex speech API. It is designed to be modular so that new use cases can be quickly added with well-encapsulated code changes.

## Instructions

| Documentation                                           | Description                                     |
| --------------------------------------------------------| ----------------------------------------------- |
| [Getting Started](./docs/getting-started.md)            | How to get started, run locally and on cloud    |
| [Adding a new Agent](./docs/adding-a-new-agent.md)      | How to build and test a new agent               |
| [Testing and Developing Agents](./docs/testing-and-developing.md) | Test and develop your agent           |
| [Contributing](../docs/contributing.md)                  | How to contribute to this project               |
| [Code of Conduct](../docs/code-of-conduct.md)            | Code of conduct for contributors                |


## Cloud deployment
To deploy this project to an App Engine instance, set up your cloud project and authenticate as per [Getting Started](./docs/getting-started.md). Then run:

```sh
# Builds the client and puts generated bundles in the server/dist directory.
cd client
npm run prod

# Deploys client and server to App Engine
cd ../server
gcloud app deploy
```
