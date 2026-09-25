# Zepto Data & AI Platform

## Project Overview

This project is an end-to-end Data Analytics and AI/ML platform developed as part of the Certificate Program in Artificial Intelligence and Machine Learning.

The project consists of three modules:

1. **Data Pipeline:** Scrapes book data, cleans and stores it in a SQLite database, and performs SQL-based analysis.
2. **Analytics:** Performs exploratory data analysis and builds a machine learning model using the Titanic dataset.
3. **Support Assistant:** Builds an offline RAG-based customer support assistant using Zepto policy documents, embeddings, ChromaDB, LangGraph, and FastAPI.

## Project Structure

```text
zepto-ai-ml-capstone/
├── data_pipeline/
├── analytics/
├── support_assistant/
└── README.md
```

## Setup and Installation

### Prerequisites
- Python 3.13
- Git
- Docker Desktop (for running the Support Assistant in Docker)

### 1. Clone the Repository

```bash
git clone https://github.com/Kammili-Kalyan/zepto-ai-ml-capstone.git
cd zepto-ai-ml-capstone

### Create and Activate a Virtual Environment
   python -m venv .venv

  On Windows PowerShell:

  .\.venv\Scripts\Activate.ps1

### Install Dependencies

 Install the dependencies required for each module using its respective requirements.txt file, if available.


**Important:** This section is a starting point. We’ll add the exact dependency installation commands after checking which `requirements.txt` files are present.


## Modules and Design Decisions

### Module 1: Data Pipeline

**Objective:** Collect, clean, transform, and store book data from Books to Scrape.

**Key features:**
- Scrapes 60 books from 3 categories.
- Cleans and transforms price, rating, and availability data.
- Converts prices from GBP to INR.
- Stores data in a normalized SQLite database.
- Uses SQL queries and pandas for data analysis.

**Design decisions:**
- SQLite is used for lightweight, local data storage.
- Separate tables for books and categories help organize the data.
- Pandas is used to compare and analyze the stored data.

### Module 2: Analytics

**Objective:** Perform exploratory data analysis and build a machine learning model using the Titanic dataset.

**Key features:**
- Exploratory data analysis (EDA).
- Data preprocessing and feature engineering.
- Model training and prediction.
- Model evaluation.

**Design decisions:**
- Jupyter notebooks are used for step-by-step analysis.
- The workflow separates data exploration from model building.

### Module 3: Support Assistant

**Objective:** Build an offline RAG-based customer support assistant using Zepto policy documents.

**Key features:**
- Uses 8 policy documents as its knowledge base.
- Generates embeddings using `all-MiniLM-L6-v2`.
- Stores embeddings in ChromaDB.
- Uses LangGraph for workflow orchestration.
- Provides a FastAPI `/ask` endpoint.
- Supports offline mock responses.

**Design decisions:**
- Local embeddings and ChromaDB support offline retrieval.
- LangGraph separates intent classification, retrieval, and direct responses.
- FastAPI provides an interface for asking questions.
- Mock mode allows the assistant to run without a paid LLM service.


## How to Run Each Module

### Module 1: Data Pipeline

Run the data pipeline from the project root:

```bash
python data_pipeline/database.py

SQL queries are available in data_pipeline/queries.sql.

### Module 2: Analytics

Open the Jupyter notebooks in the analytics/ folder:

**01_eda.ipynb — Exploratory Data Analysis

**02_modeling.ipynb — Model Building and Evaluation

Run the notebook cells in order to complete the workflow.

### Module 3: Support Assistant

Step 1: Install Dependencies
**pip install -r support_assistant/requirements.txt

Step 2: Ingest Policy Documents
**python support_assistant/ingest.py

Step 3: Run the Support Assistant
**python -m support_assistant.run

Step 4: Run with Docker
Build the Docker image:
**docker build -f support_assistant/Dockerfile -t zepto-support-assistant .

Run the container:
**docker run -p 7860:7860 zepto-support-assistant


## API Testing Examples

The Support Assistant provides a `POST /ask` endpoint that accepts a customer query and returns an answer, source documents, and a confidence score.

### Example 1: Policy Question

**Request:**

```json
{
  "query": "What is the delivery fee for orders below INR 149?"
}

**Expected response:**
{
  "answer": "Based on the retrieved context: ...",
  "sources": [
    "doc_01.txt"
  ],
  "confidence": 0.9
}

**Request:**
{
  "query": "What is the capital of India?"
}

**Expected response:**
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}


### Testing Through Swagger UI

** Start the Support Assistant.
** Open http://127.0.0.1:8000/docs.
** Expand POST /ask.
** Click Try it out.
** Enter a JSON request and click Execute.
** Check the response body and HTTP status code.


## Configuration

### Support Assistant Mock Mode
The Support Assistant runs in offline mock mode by default.

```powershell
$env:MOCK_LLM="1"
python -m support_assistant.run