from fastapi import APIRouter

router = APIRouter()

@router.post("/jobs/{job_id}/match")
async def match_job(job_id: str):
    """Match user profile with job."""
    return {"message": "Job matching endpoint - to be implemented"}
