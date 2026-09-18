from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ApplicationBase(BaseModel):
    job_id: Optional[int] = None
    company_id: Optional[int] = None
    resume_id: Optional[int] = None
    role: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    job_url: Optional[str] = None
    application_url: Optional[str] = None
    notes: Optional[str] = None
    interview_date: Optional[datetime] = None
    next_steps: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(ApplicationBase):
    status: Optional[str] = None  # applied, assessment, interview, hr_interview, offer, rejected, withdrawn


class ApplicationResponse(ApplicationBase):
    id: int
    user_id: int
    status: str  # applied, assessment, interview, hr_interview, offer, rejected, withdrawn
    applied_date: datetime
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True


class ApplicationEventBase(BaseModel):
    event_type: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    interview_date: Optional[datetime] = None


class ApplicationEventCreate(ApplicationEventBase):
    application_id: int


class ApplicationEventResponse(ApplicationEventBase):
    id: int
    application_id: int
    event_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True
