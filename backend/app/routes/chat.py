from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agent.router import agent_router
from app.services.vector_db import vector_db
from app.services.embeddings import embedding_service
from typing import List

router = APIRouter()

class Message(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    tool: str
    source: str

chat_history = []

@router.post("/ask", response_model=ChatResponse)
async def ask_question(message: Message):
    try:
        query = message.query
        
        if not query or not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if len(vector_db.documents) == 0:
            raise HTTPException(status_code=400, detail="No documents uploaded yet")
        
        context = " ".join(vector_db.documents[:5])
        
        result = agent_router.route(query, context)
        
        chat_history.append({
            "query": query,
            "answer": result['answer'],
            "tool": result['tool']
        })
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_history():
    return {"history": chat_history}

@router.delete("/history")
async def clear_history():
    global chat_history
    chat_history = []
    return {"status": "history cleared"}