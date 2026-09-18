from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    logo_url = Column(String)
    website = Column(String)
    industry = Column(String)
    description = Column(Text)
    locations = Column(JSON)  # List of office locations
    company_size = Column(String)  # startup, small, medium, large, enterprise
    founded_year = Column(Integer)
    
    # Verification
    is_verified = Column(Boolean, default=False)
    verification_status = Column(String)  # pending, verified, rejected
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (using string references to avoid circular imports)
    jobs = relationship("Job", back_populates="company")
    interview_questions = relationship("InterviewQuestion", back_populates="company")
    coding_questions = relationship("CodingQuestion", back_populates="company")
