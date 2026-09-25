"""
Zepto Support Assistant - FastAPI

"""

from fastapi import FastAPI

from support_assistant.graph import ask_zepto, SupportResponse
from support_assistant.schemas import AskRequest,SupportResponse

# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Zepto Support Assistant",
    description="Offline RAG-based Zepto policy assistant",
    version="1.0.0"
)


# ============================================================
# POST /ask
# ============================================================

@app.post(
    "/ask",
    response_model=SupportResponse
)
def ask(request: AskRequest):

    response = ask_zepto(
        request.query
    )

    return response


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def root():

    return {
        "message": "Zepto Support Assistant is running",
        "endpoint": "POST /ask"
    }