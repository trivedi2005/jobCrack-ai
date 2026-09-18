from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ResumeBase(BaseModel):
    original_filename: Optional[str] = None
    file_type: Optional[str] = None


class ResumeCreate(ResumeBase):
    pass


class ResumeResponse(ResumeBase):
    id: int
    user_id: int
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    is_current: bool
    version: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ResumeAnalysisRequest(BaseModel):
    resume_id: int
    job_id: Optional[int] = None


class ResumeAnalysisResponse(BaseModel):
    id: int
    resume_id: int
    job_id: Optional[int] = None
    keyword_score: Optional[float] = None
    structure_score: Optional[float] = None
    formatting_score: Optional[float] = None
    overall_score: Optional[float] = None
    matched_keywords: Optional[list] = None
    missing_keywords: Optional[list] = None
    suggested_improvements: Optional[list] = None
    skill_gaps: Optional[list] = None
    job_match_score: Optional[float] = None
    experience_match: Optional[Dict[str, Any]] = None
    education_match: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ResumeTailorRequest(BaseModel):
    resume_id: int
    job_id: int
    suggestions: Optional[list] = None


class ResumeVersionResponse(BaseModel):
    id: int
    resume_id: int
    job_id: Optional[int] = None
    version_name: Optional[str] = None
    is_ai_tailored: Optional[bool] = None
    created_at: datetime

    class Config:
        from_attributes = True
