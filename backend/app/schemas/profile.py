from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProfileBase(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    current_city: Optional[str] = None
    preferred_locations: Optional[List[str]] = None
    target_roles: Optional[List[str]] = None
    experience_years: Optional[int] = 0
    preferred_work_mode: Optional[str] = None
    preferred_salary_min: Optional[int] = None
    preferred_salary_max: Optional[int] = None
    job_type: Optional[str] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    profile_completeness: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EducationBase(BaseModel):
    degree: Optional[str] = None
    branch: Optional[str] = None
    institution: Optional[str] = None
    university: Optional[str] = None
    graduation_year: Optional[int] = None
    cgpa_percentage: Optional[float] = None


class EducationCreate(EducationBase):
    pass


class EducationResponse(EducationBase):
    id: int
    profile_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None


class SkillCreate(SkillBase):
    pass


class SkillResponse(SkillBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserSkillBase(BaseModel):
    skill_id: int
    proficiency_level: Optional[str] = None
    years_of_experience: Optional[int] = 0


class UserSkillCreate(UserSkillBase):
    pass


class UserSkillResponse(UserSkillBase):
    id: int
    profile_id: int
    skill_name: str
    created_at: datetime

    class Config:
        from_attributes = True
