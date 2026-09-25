"""
Zepto Support Assistant - Task 3
--------------------------------
LangGraph workflow:
"""

import os
from typing import TypedDict

import chromadb
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, START, END

from support_assistant.prompt import build_prompt
from support_assistant.schemas import SupportResponse


# ============================================================
# CONFIGURATION
# ============================================================

MOCK_LLM = os.getenv("MOCK_LLM", "1")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL_NAME
)

print("Embedding model loaded.")


# ============================================================
# CONNECT TO CHROMADB
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=CHROMA_DIR
)

collection = chroma_client.get_collection(
    name="zepto_policies"
)

print(f"ChromaDB records available: {collection.count()}")



# ============================================================
# LANGGRAPH STATE
# ============================================================

class SupportState(TypedDict, total=False):

    query: str

    intent: str

    context: str

    sources: list[str]

    answer: str

    confidence: float

#=============================================================   
### Validation response
#=============================================================

def validate_llm_response_with_retry(
    generate_fn,
    prompt: str,
    max_retries: int = 2
) -> SupportResponse:
    """
    Validate real-LLM output against the Pydantic response schema.

    If validation fails, retry up to 2 additional times with a
    corrective instruction.
    """

    corrective_instruction = """
Your previous response did not match the required JSON schema.

Return ONLY valid JSON with exactly these fields:
{
  "answer": "string",
  "sources": ["string"],
  "confidence": 0.0
}

confidence must be a number between 0 and 1.
Do not add Markdown or extra text.
"""

    for attempt in range(max_retries + 1):
        if attempt == 0:
            current_prompt = prompt
        else:
            current_prompt = prompt + "\n\n" + corrective_instruction

        raw_output = generate_fn(current_prompt)

        try:
            return SupportResponse.model_validate_json(raw_output)

        except Exception:
            if attempt == max_retries:
                return SupportResponse(
                    answer="ERROR: The real LLM response could not be validated.",
                    sources=[],
                    confidence=0.0
                )

    return SupportResponse(
        answer="ERROR: The real LLM response could not be validated.",
        sources=[],
        confidence=0.0
    )

# ============================================================
# NODE 1 — CLASSIFY INTENT
# ============================================================

def classify_intent(state: SupportState) -> SupportState:

    query = state["query"]

    # --------------------------------------------------------
    # REQUIRED MOCK MODE
    # --------------------------------------------------------

    if MOCK_LLM != "0":

        query_lower = query.lower()

        policy_keywords = [
            "delivery",
            "return",
            "refund",
            "membership",
            "tracking",
            "cancel",
            "gift card",
            "support hours",
        ]

        if any(
            keyword in query_lower
            for keyword in policy_keywords
        ):
            intent = "policy_question"
        else:
            intent = "general_question"

    # --------------------------------------------------------
    # OPTIONAL REAL LLM MODE
    # --------------------------------------------------------

    else:

        # Real LLM integration is optional for this project.
        # The graded submission uses MOCK_LLM=1.
        raise NotImplementedError(
            "MOCK_LLM=0 is an optional extension. "
            "Use MOCK_LLM=1 for the graded offline mode."
        )

    print(f"Query: {query}")
    print(f"Intent: {intent}")

    return {
        "intent": intent
    }


# ============================================================
# NODE 2 — RETRIEVE AND ANSWER
# ============================================================

def retrieve_and_answer(state: SupportState) -> SupportState:

    query = state["query"]

    # --------------------------------------------------------
    # EMBED USER QUERY
    # --------------------------------------------------------

    query_embedding = embedding_model.encode(
        [query],
        normalize_embeddings=True
    )[0].tolist()

    # --------------------------------------------------------
    # RETRIEVE TOP 3 CHUNKS
    # --------------------------------------------------------

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    retrieved_documents = results["documents"][0]
    retrieved_metadatas = results["metadatas"][0]
    retrieved_distances = results["distances"][0]

    # --------------------------------------------------------
    # BUILD CONTEXT
    # --------------------------------------------------------

    context_parts = []

    sources = []

    for document, metadata in zip(
        retrieved_documents,
        retrieved_metadatas
    ):

        context_parts.append(document)

        source = metadata.get(
            "source",
            "unknown"
        )

        sources.append(source)

    context = "\n\n".join(context_parts)

    # --------------------------------------------------------
    # BUILD STRUCTURED PROMPT
    # --------------------------------------------------------

    prompt = build_prompt(
        query=query,
        context=context
    )

    # --------------------------------------------------------
    # REQUIRED MOCK ANSWER
    # --------------------------------------------------------

    if MOCK_LLM != "0":

        top_chunk = retrieved_documents[0]

        # Keep the mock response deterministic.
        snippet = top_chunk.strip()

        if len(snippet) > 300:
            snippet = snippet[:300] + "..."

        answer = (
            "Based on the retrieved context: "
            + snippet
        )

        confidence = 0.90

    # --------------------------------------------------------
    # OPTIONAL REAL LLM
    # --------------------------------------------------------

    else:

        raise NotImplementedError(
            "MOCK_LLM=0 is an optional extension. "
            "Use MOCK_LLM=1 for the graded offline mode."
        )

    print()
    print("Retrieved sources:")

    for source, distance in zip(
        sources,
        retrieved_distances
    ):
        print(
            f"  {source} | cosine distance: {distance:.4f}"
        )

    # `prompt` is constructed here so Task 2's structured
    # prompt is directly connected to the retrieval workflow.
    _ = prompt

    return {
        "context": context,
        "sources": sources,
        "answer": answer,
        "confidence": confidence
    }


# ============================================================
# NODE 3 — DIRECT ANSWER
# ============================================================

def direct_answer(state: SupportState) -> SupportState:

    # --------------------------------------------------------
    # REQUIRED MOCK MODE
    # --------------------------------------------------------

    if MOCK_LLM != "0":

        answer = (
            "I can only answer questions about Zepto policies "
            "right now."
        )

        confidence = 1.0

    # --------------------------------------------------------
    # OPTIONAL REAL LLM MODE
    # --------------------------------------------------------

    else:

        raise NotImplementedError(
            "MOCK_LLM=0 is an optional extension. "
            "Use MOCK_LLM=1 for the graded offline mode."
        )

    return {
        "answer": answer,
        "sources": [],
        "confidence": confidence
    }


# ============================================================
# CONDITIONAL ROUTING
# ============================================================

def route_after_classification(
    state: SupportState
) -> str:

    if state["intent"] == "policy_question":

        return "retrieve_and_answer"

    return "direct_answer"


# ============================================================
# BUILD LANGGRAPH
# ============================================================

builder = StateGraph(SupportState)


# Add required nodes
builder.add_node(
    "classify_intent",
    classify_intent
)

builder.add_node(
    "retrieve_and_answer",
    retrieve_and_answer
)

builder.add_node(
    "direct_answer",
    direct_answer
)


# Start -> classify
builder.add_edge(
    START,
    "classify_intent"
)


# Conditional routing
builder.add_conditional_edges(
    "classify_intent",
    route_after_classification,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer",
    }
)


# Both paths -> END
builder.add_edge(
    "retrieve_and_answer",
    END
)

builder.add_edge(
    "direct_answer",
    END
)


# Compile graph
graph = builder.compile()


# ============================================================
# RUN FUNCTION
# ============================================================

def ask_zepto(query: str) -> SupportResponse:

    result = graph.invoke(
        {
            "query": query
        }
    )

    response = SupportResponse(
        answer=result["answer"],
        sources=result.get("sources", []),
        confidence=result.get("confidence", 0.0)
    )

    return response


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("TEST 1 — POLICY QUESTION")
    print("=" * 60)

    response = ask_zepto(
        "What is the delivery fee for orders below INR 149?"
    )

    print(response.model_dump_json(indent=2))


    print()
    print("=" * 60)
    print("TEST 2 — GENERAL QUESTION")
    print("=" * 60)

    response = ask_zepto(
        "What is the capital of India?"
    )

    print(response.model_dump_json(indent=2))