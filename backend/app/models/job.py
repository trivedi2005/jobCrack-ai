from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class JobType(str, enum.Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    INTERNSHIP = "internship"
    CONTRACT = "contract"
    FREELANCE = "freelance"


class WorkMode(str, enum.Enum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"


class ExperienceLevel(str, enum.Enum):
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    FRESHER = "fresher"


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    
    # Job Details
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    requirements = Column(Text)
    responsibilities = Column(Text)
    
    # Location & Type
    location = Column(String, index=True)
    job_type = Column(Enum(JobType), default=JobType.FULL_TIME)
    work_mode = Column(Enum(WorkMode), default=WorkMode.ONSITE)
    experience_level = Column(Enum(ExperienceLevel), default=ExperienceLevel.ENTRY)
    experience_years_min = Column(Integer)
    experience_years_max = Column(Integer)
    
    # Compensation
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    salary_currency = Column(String, default="INR")
    salary_period = Column(String)  # annual, monthly, hourly
    
    # Skills & Requirements
    required_skills = Column(JSON)  # List of skill IDs
    preferred_skills = Column(JSON)  # List of skill IDs
    
    # Application
    application_url = Column(String)
    application_email = Column(String)
    apply_deadline = Column(DateTime)
    
    # Source & Verification
    source = Column(String)  # internal, api, scraped, manual
    source_url = Column(String)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_status = Column(String)  # pending, verified, rejected
    
    # Metadata
    posted_date = Column(DateTime(timezone=True), server_default=func.now())
    expiry_date = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (using string references to avoid circular imports)
    company = relationship("Company", back_populates="jobs")
    job_skills = relationship("JobSkill", back_populates="job")
    job_matches = relationship("JobMatch", back_populates="job")
    applications = relationship("Application", back_populates="job")


class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    is_required = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships (using string references to avoid circular imports)
    job = relationship("Job", back_populates="job_skills")
    skill = relationship("Skill", back_populates="job_skills")
