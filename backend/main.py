from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

from openai_service import get_chat_completion

# Load environment variables
load_dotenv()

app = FastAPI(title="Chatbot API with Arize Phoenix Tracing")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = "gpt-3.5-turbo"

class ChatResponse(BaseModel):
    message: Message
    trace_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat request and return a response from the AI model.
    The request is traced using Arize Phoenix.
    """
    try:
        # Convert Pydantic models to dictionaries for the OpenAI API
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Get response from OpenAI
        response, trace_id = await get_chat_completion(messages, request.model)
        
        return ChatResponse(
            message=Message(role="assistant", content=response),
            trace_id=trace_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)