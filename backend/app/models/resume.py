from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # File Information
    original_filename = Column(String)
    file_path = Column(String)
    file_size = Column(Integer)
    file_type = Column(String)  # pdf, docx
    
    # Parsed Content
    parsed_data = Column(JSON)  # Extracted name, skills, experience, etc.
    
    # Current Version
    is_current = Column(Boolean, default=True)
    version = Column(Integer, default=1)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (using string references to avoid circular imports)
    user = relationship("User", back_populates="resumes")
    versions = relationship("ResumeVersion", back_populates="resume")
    analyses = relationship("ResumeAnalysis", back_populates="resume")


class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)
    
    # Version Details
    version_name = Column(String)  # "Original", "Company X", "AI/ML", etc.
    content = Column(Text)  # Full resume content
    changes = Column(JSON)  # List of changes made
    
    # AI Tailoring
    is_ai_tailored = Column(Boolean, default=False)
    tailoring_job_id = Column(Integer, ForeignKey("jobs.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships (using string references to avoid circular imports)
    resume = relationship("Resume", back_populates="versions")


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)
    
    # ATS Scores
    keyword_score = Column(Float)
    structure_score = Column(Float)
    formatting_score = Column(Float)
    overall_score = Column(Float)
    
    # Analysis Details
    matched_keywords = Column(JSON)
    missing_keywords = Column(JSON)
    suggested_improvements = Column(JSON)
    skill_gaps = Column(JSON)
    
    # Job Match
    job_match_score = Column(Float)
    experience_match = Column(JSON)
    education_match = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships (using string references to avoid circular imports)
    resume = relationship("Resume", back_populates="analyses")
