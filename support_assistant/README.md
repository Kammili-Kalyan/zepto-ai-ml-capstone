## Module 3 — Support Assistant

### RAG Architecture

The Support Assistant uses a Retrieval-Augmented Generation (RAG) pipeline
to answer questions using the provided Zepto policy documents.

The pipeline follows:

**Ingestion → Embedding → Retrieval → Generation**

#### 1. Ingestion

The 8 Zepto policy documents are stored as `.txt` files inside:

`support_assistant/docs/`

The `ingest.py` file reads all 8 documents and loads their contents into
memory. Each document is assigned an ID based on its filename, and the
filename is stored as source metadata.

The ingestion process stores the documents in a persistent ChromaDB
collection named:

`zepto_policies`

#### 2. Embedding

The `ingest.py` file uses the local
`all-MiniLM-L6-v2` model from `sentence-transformers` to create embeddings
for all 8 policy documents.

The embeddings are normalized and stored in ChromaDB using cosine
similarity.

No external embedding API is required.

The stored vector database is:

`support_assistant/chroma_db/`

#### 3. Retrieval

User questions are processed by the LangGraph workflow in `graph.py`.

The `classify_intent` node first determines whether the question is a
policy question or a general question.

Policy questions are routed to the `retrieve_and_answer` node.

The `retrieve_and_answer` node:

1. Converts the user's question into an embedding using
   `all-MiniLM-L6-v2`.
2. Queries the `zepto_policies` ChromaDB collection.
3. Retrieves the most relevant policy documents using cosine similarity.
4. Builds the context from the retrieved documents.
5. Passes the retrieved context to the answer-generation step.

General questions are routed directly to the `direct_answer` node without
retrieval.

#### 4. Generation

The generation logic is implemented inside the LangGraph nodes in
`graph.py`.

For a policy question, `retrieve_and_answer` generates the final answer
from the most relevant retrieved context.

For a general question, `direct_answer` returns the fixed response used by
the offline mock mode.

The structured prompt template used by the optional real-LLM path is
defined in:

`support_assistant/prompt.py`

The prompt contains the required role, context, task, format, length,
negative constraint, and few-shot example.

### LangGraph Workflow

The workflow contains three nodes:

`classify_intent` — classifies the incoming query.
`retrieve_and_answer` — retrieves relevant policy documents and prepares an answer.
`direct_answer` — returns a fixed response for general questions.

Conditional routing sends policy questions to retrieval and general questions to the direct-answer node.

## Mock Mode

The application uses MOCK_LLM=1 by default.

MOCK_LLM=1: Runs the offline mock response logic.
MOCK_LLM=0: Selects the optional real-LLM path, if configured.

The offline mock mode is the required baseline and does not need an LLM API key.

## Setup and Installation

Run these commands from the project root.

# Create a virtual environment
py -3.13 -m venv .venv

# Activate the environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r support_assistant\requirements.txt

## Run the Application Locally

First, ingest the policy documents:

"""python support_assistant\ingest.py"""

Start the FastAPI application:

"""python -m support_assistant.run"""

The Swagger UI opens at:

http://127.0.0.1:8000/docs

Use the POST /ask endpoint to submit questions.

## Docker Deployment

Build the Docker image from the project root:

"""docker build -f support_assistant/Dockerfile -t zepto-support-assistant ."""

Run the container:

"""docker run -p 7860:7860 zepto-support-assistant"""

Open Swagger UI:

http://127.0.0.1:7860/docs

To stop the container, press Ctrl+C if running in the foreground.

### Design Decisions
*Local embeddings: all-MiniLM-L6-v2 avoids the need for a paid embedding API.
*ChromaDB: Stores document vectors and supports similarity-based retrieval.
*LangGraph: Separates intent classification, retrieval, and direct responses into distinct nodes.
*Pydantic: Validates the response structure and confidence range.
*FastAPI: Provides a simple API for testing the assistant.
*Docker: Packages the application and its dependencies into a container.
*Offline mock mode: Keeps the required application deterministic and usable without an external 
 LLM service.

### Data Flow

```text
8 Zepto Policy Documents
          |
          v
      ingest.py
          |
          v
 all-MiniLM-L6-v2
      Embeddings
          |
          v
      ChromaDB
  "zepto_policies"
          |
          |
     User Question
          |
          v
    classify_intent
       /       \
      /         \
 Policy        General
 Question      Question
    |              |
    v              v
retrieve_and_    direct_answer
answer
    |
    v
Retrieved Context
    |
    v
Generation
    |
    v
Pydantic Response
(answer, sources, confidence)


## Limitations

The required mock mode uses deterministic response logic rather than a generative LLM. Its answers are based on retrieved policy text, and general questions receive a fixed response. The application is designed to answer questions about the supplied Zepto policy documents.
