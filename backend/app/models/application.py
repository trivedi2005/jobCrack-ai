from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class ApplicationStatus(str, enum.Enum):
    APPLIED = "applied"
    ASSESSMENT = "assessment"
    INTERVIEW = "interview"
    HR_INTERVIEW = "hr_interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="SET NULL"), nullable=True)
    
    # Application Details
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED)
    role = Column(String)
    company = Column(String)
    location = Column(String)
    
    # Application Links
    job_url = Column(String)
    application_url = Column(String)
    
    # Notes
    notes = Column(Text)
    interview_date = Column(DateTime)
    next_steps = Column(Text)
    
    # Metadata
    applied_date = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (using string references to avoid circular imports)
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
    events = relationship("ApplicationEvent", back_populates="application")


class ApplicationEvent(Base):
    __tablename__ = "application_events"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    
    # Event Details
    event_type = Column(String)  # applied, assessment, interview, offer, rejected, note
    status = Column(String)
    description = Column(Text)
    notes = Column(Text)
    
    # Dates
    event_date = Column(DateTime(timezone=True), server_default=func.now())
    interview_date = Column(DateTime)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships (using string references to avoid circular imports)
    application = relationship("Application", back_populates="events")
