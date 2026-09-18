from fastapi import APIRouter

router = APIRouter()

@router.get("/problems")
async def get_coding_problems():
    """Get coding problems."""
    return {"message": "Get coding problems endpoint - to be implemented"}
