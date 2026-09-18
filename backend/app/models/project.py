from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String)
    description = Column(Text)
    technologies = Column(String)  # Comma-separated list
    project_url = Column(String)
    github_url = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (using string references to avoid circular imports)
    profile = relationship("Profile", back_populates="projects")
