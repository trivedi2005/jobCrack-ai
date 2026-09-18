from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class QuestionDifficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class CodingQuestion(Base):
    __tablename__ = "coding_questions"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    
    # Problem Details
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(Enum(QuestionDifficulty), default=QuestionDifficulty.MEDIUM)
    topics = Column(JSON)  # List of topics (arrays, strings, dp, etc.)
    
    # Problem Constraints
    time_limit = Column(Integer)  # in seconds
    memory_limit = Column(Integer)  # in MB
    constraints = Column(Text)
    
    # Examples
    examples = Column(JSON)  # List of example input/output pairs
    
    # Solution
    solution = Column(Text)
    solution_approach = Column(Text)
    time_complexity = Column(String)
    space_complexity = Column(String)
    
    # Tags
    tags = Column(JSON)  # company tags, topic tags
    
    # Metadata
    acceptance_rate = Column(Float)
    total_submissions = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (using string references to avoid circular imports)
    company = relationship("Company", back_populates="coding_questions")
