from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_notifications():
    """Get user notifications."""
    return {"message": "Get notifications endpoint - to be implemented"}
