from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CompanyBase(BaseModel):
    name: str
    logo_url: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    locations: Optional[List[str]] = None
    company_size: Optional[str] = None
    founded_year: Optional[int] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    id: int
    is_verified: bool
    verification_status: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CompanyDetailResponse(CompanyResponse):
    current_jobs_count: Optional[int] = 0
    interview_questions_count: Optional[int] = 0
    coding_questions_count: Optional[int] = 0
