from fastapi import APIRouter

router = APIRouter()

@router.post("/start")
async def start_interview():
    """Start AI mock interview."""
    return {"message": "Start interview endpoint - to be implemented"}
