from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_applications():
    """Get user applications."""
    return {"message": "Get applications endpoint - to be implemented"}

@router.post("/")
async def create_application():
    """Create application."""
    return {"message": "Create application endpoint - to be implemented"}
