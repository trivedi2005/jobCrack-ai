from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class JobMatchResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    overall_score: Optional[float] = None
    skills_score: Optional[float] = None
    experience_score: Optional[float] = None
    education_score: Optional[float] = None
    location_score: Optional[float] = None
    matched_skills: Optional[List[str]] = None
    missing_skills: Optional[List[str]] = None
    relevant_experience: Optional[List[Dict[str, Any]]] = None
    skill_gaps: Optional[List[Dict[str, Any]]] = None
    suggested_preparation: Optional[List[str]] = None
    resume_match_score: Optional[float] = None
    resume_gaps: Optional[List[str]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class JobMatchRequest(BaseModel):
    job_id: int
