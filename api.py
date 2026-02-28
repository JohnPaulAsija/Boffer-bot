from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from goog import init_ai_client, generate_response

app = FastAPI(title="Boffer Bot API", description="LARP rules chatbot API")

# Global state - will be initialized at startup
client = None
system_instructions = None
rules_file_refs = None


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


@app.on_event("startup")
async def startup_event():
    """Initialize the Gemini AI client at startup."""
    global client, system_instructions, rules_file_refs
    try:
        client, system_instructions, rules_file_refs = init_ai_client()
        print("AI client initialized successfully")
    except Exception as e:
        print(f"Failed to initialize AI client: {e}")
        raise


@app.get("/health")
async def health():
    """Health check endpoint for monitoring."""
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Ask a question about LARP rules.

    The bot will search the rulebooks and provide a grounded answer.
    """
    if not client or not system_instructions or rules_file_refs is None:
        raise HTTPException(
            status_code=503,
            detail="AI client not initialized. Please try again later."
        )

    try:
        answer = generate_response(
            prompt=request.question,
            client=client,
            system_instructions=system_instructions,
            rules_file_refs=rules_file_refs
        )
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}"
        )
