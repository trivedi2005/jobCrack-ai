from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    
    # Match Scores
    overall_score = Column(Float)
    skills_score = Column(Float)
    experience_score = Column(Float)
    education_score = Column(Float)
    location_score = Column(Float)
    
    # Match Details
    matched_skills = Column(JSON)
    missing_skills = Column(JSON)
    relevant_experience = Column(JSON)
    skill_gaps = Column(JSON)
    suggested_preparation = Column(JSON)
    
    # Resume Analysis
    resume_match_score = Column(Float)
    resume_gaps = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (using string references to avoid circular imports)
    job = relationship("Job", back_populates="job_matches")
