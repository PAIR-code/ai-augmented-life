# Getting Started
This project consists of two components:

* server - a Python server for communication with Cloud APIs
* client — an Angular Web application

It uses the [Cloud Vertex APIs](https://cloud.google.com/vertex-ai) for language-model calls and the [Cloud Text-To-Speech API](https://cloud.google.com/text-to-speech) to generate audio from the language model text output. This project can be run locally or as an [App Engine project](https://cloud.google.com/appengine/) but both configurations require a Google Cloud project to run correctly.

## Cloud set-up
There are a few steps to this and some familiarity with Google Cloud is assumed:

1. Create a [Google Cloud project](https://cloud.google.com/cloud-console) and enable the [Vertex AI APIs](https://cloud.google.com/vertex-ai/generative-ai/docs/start/quickstarts/quickstart-multimodal). 

2. Follow [Google Cloud Installation Instructions](https://cloud.google.com/sdk/docs/install) to install the Google Cloud CLI.

3. Follow [Set up Application Default Credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc) to set up application default credentials.

On the command line, configure your local GCloud environment and log-in with application default credentials so your local server can access the APIs in your Cloud project:

```sh
gcloud auth login
gcloud config set project [PROJECT_ID]
gcloud auth application-default login
gcloud auth application-default set-quota-project [PROJECT_ID]
```

## Server:
To run the server locally:

```sh
 cd server
 python3 -m venv . # create and activate virtual environment
 source bin/activate
 pip3 install -r requirements.txt
 python3 main.py
 deactivate # deactivate the virtual environment when done
```

You can verify that the server is running by pointing your browser at:
http://localhost:8080/chat?q=hello

## Client:
Install npm at: https://nodejs.org/en/download/ if necessary.

Then:
```sh
cd client
npm install
npm run start
```

Navigate to http://localhost:4200 and click the microphone icon to begin speaking. The supported agents can be found in the app drawer on the left-hand-side. Each agent maps to a specific Angular component on the client for custom fronend UI and a specific Python module on the server for custom prompts, chains, or integrations.

The goal is to make it easy and well-encapsulated to add new agents that are configured to perform specific tasks in order to explore the range of possible new use-cases for voice-powered agents.

## Run Tests
<span style="color:red">**WARNING**:</span> Some tests make multiple calls to the Cloud Vertex APIs and will incur charges to your Cloud project.

### Client tests:
```sh
cd client
npm run ng test
```

### Server tests:
```sh
cd server

# All tests
python3 -m unittest discover -t . -s . -p "*_test.py"

# A specific test
python3 -m unittest agents.fake_agent_test
```

**Note**: Large language models (LLMs) are inherently non-determinate and so any tests that make calls to them are inherently flaky. If you see an AssertionError of
the form ```Evaluation of model response failed.``` it is likely a flaky test and doesn't indicate a problem with your build.

If you're building an agent and want to assess the overall success rate for flaky tests
you can use the ```run_tests.py``` convenience script to run each test multiple times.
```sh
cd server

# For all tests in a suite
python3 -m scripts.run_tests --test_name fake_agent_test --run_count=10

# For a specific test
python3 -m scripts.run_tests --test_name fake_agent_test.test_chat --run_count=10
```

A fuller discussion of building and testing agents can be found in [Adding a New Agent](./adding-a-new-agent.md)

## Contributing

Before submitting a pull request ensure formatting and linting run correctly:

```sh
cd server
pylint .
black .
```
