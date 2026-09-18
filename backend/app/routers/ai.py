from fastapi import APIRouter

router = APIRouter()

@router.post("/chat")
async def ai_chat():
    """AI Career Copilot chat."""
    return {"message": "AI chat endpoint - to be implemented"}
