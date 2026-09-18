from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Personal Information
    full_name = Column(String)
    phone = Column(String)
    current_city = Column(String)
    preferred_locations = Column(JSON)  # List of cities
    
    # Career Information
    target_roles = Column(JSON)  # List of target roles
    experience_years = Column(Integer, default=0)
    preferred_work_mode = Column(String)  # remote, hybrid, onsite
    preferred_salary_min = Column(Integer)
    preferred_salary_max = Column(Integer)
    job_type = Column(String)  # full-time, part-time, internship, contract
    
    # Profile completeness
    profile_completeness = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (using string references to avoid circular imports)
    user = relationship("User", back_populates="profile")
    education = relationship("Education", back_populates="profile")
    skills = relationship("UserSkill", back_populates="profile")
    experiences = relationship("Experience", back_populates="profile")
    projects = relationship("Project", back_populates="profile")
    certifications = relationship("Certification", back_populates="profile")
