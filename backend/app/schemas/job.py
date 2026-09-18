from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class JobBase(BaseModel):
    title: str
    description: Optional[str] = None
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = "full-time"  # full-time, part-time, internship, contract
    work_mode: Optional[str] = "onsite"  # remote, hybrid, onsite
    experience_level: Optional[str] = "entry"  # entry, mid, senior, lead, fresher
    experience_years_min: Optional[int] = None
    experience_years_max: Optional[int] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: Optional[str] = "INR"
    salary_period: Optional[str] = None
    required_skills: Optional[List[int]] = None
    preferred_skills: Optional[List[int]] = None
    application_url: Optional[str] = None
    application_email: Optional[str] = None
    apply_deadline: Optional[datetime] = None


class JobCreate(JobBase):
    company_id: int


class JobUpdate(JobBase):
    pass


class JobResponse(JobBase):
    id: int
    company_id: int
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    is_active: bool
    is_verified: bool
    posted_date: datetime
    expiry_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class JobListResponse(BaseModel):
    id: int
    title: str
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    work_mode: Optional[str] = None
    experience_level: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: Optional[str] = None
    posted_date: datetime
    match_percentage: Optional[float] = None

    class Config:
        from_attributes = True


class JobFilter(BaseModel):
    search: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    work_mode: Optional[str] = None
    experience_level: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    skills: Optional[List[int]] = None
    company_id: Optional[int] = None
    sort_by: Optional[str] = "relevance"  # relevance, newest, match
