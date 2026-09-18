from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    
    degree = Column(String)  # B.Tech, M.Tech, BCA, MCA, etc.
    branch = Column(String)  # Computer Science, IT, etc.
    institution = Column(String)
    university = Column(String)
    graduation_year = Column(Integer)
    cgpa_percentage = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (using string references to avoid circular imports)
    profile = relationship("Profile", back_populates="education")
