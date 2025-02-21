## Introduction

The Retrieval-Augmented Generation (RAG) API for the [GameRules App](https://github.com/achaturv-hub/game-rules) made by integrating Langchain, Chroma, and Ollama.

## Getting Started

1. Go to the root directory and install dependencies.

`$ pip3 install -r ./requirements.txt`

2. Update the constants.py file to account for whether Ollama is running locally or on a different machine. 
Ensure that the file is properly configured based on the environment, adjusting any relevant settings or endpoints accordingly.

3. Start API server

`$ python ./main.py`

4. The server is run on https://localhost:8000 by default.

## Built With 

- [Python](https://www.python.org/) 
- [Langchain](https://nextjs.org/) - LLM framework
- [Ollama](https://ollama.com/) - Platform for running LLMs
- [Chroma](https://www.trychroma.com/) -Vector database

## Author

Anush Chaturvedi 

https://portfolio.anushchat.dev