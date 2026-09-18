from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class QuestionDifficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class InterviewRound(str, enum.Enum):
    APTITUDE = "aptitude"
    CODING = "coding"
    TECHNICAL = "technical"
    HR = "hr"
    BEHAVIORAL = "behavioral"
    MANAGERIAL = "managerial"


class VerificationStatus(str, enum.Enum):
    OFFICIAL = "official"
    VERIFIED = "verified"
    COMMUNITY_REPORTED = "community_reported"
    EDITORIAL = "editorial"


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    
    # Question Details
    question = Column(Text, nullable=False)
    answer = Column(Text)
    explanation = Column(Text)
    
    # Categorization
    round = Column(Enum(InterviewRound))
    topic = Column(String)
    difficulty = Column(Enum(QuestionDifficulty), default=QuestionDifficulty.MEDIUM)
    role = Column(String)  # Software Engineer, Data Analyst, etc.
    
    # Source & Verification
    source = Column(String)
    verification_status = Column(Enum(VerificationStatus), default=VerificationStatus.COMMUNITY_REPORTED)
    verified_by = Column(Integer, ForeignKey("users.id"))
    
    # Usage
    times_asked = Column(Integer, default=0)
    last_asked = Column(DateTime)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships (using string references to avoid circular imports)
    company = relationship("Company", back_populates="interview_questions")


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    
    # Session Details
    interview_type = Column(String)  # technical, hr, behavioral, coding, full
    role = Column(String)
    difficulty = Column(Enum(QuestionDifficulty), default=QuestionDifficulty.MEDIUM)
    status = Column(String)  # in_progress, completed, abandoned
    
    # Results
    score = Column(Integer)
    feedback = Column(JSON)  # AI-generated feedback
    technical_feedback = Column(Text)
    communication_feedback = Column(Text)
    problem_solving_feedback = Column(Text)
    
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime)

    # Relationships (using string references to avoid circular imports)
    user = relationship("User", back_populates="interview_sessions")
    answers = relationship("InterviewAnswer", back_populates="session")


class InterviewAnswer(Base):
    __tablename__ = "interview_answers"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("interview_questions.id", ondelete="SET NULL"), nullable=True)
    
    question = Column(Text)
    answer = Column(Text)
    ai_feedback = Column(Text)
    score = Column(Integer)
    
    asked_at = Column(DateTime(timezone=True), server_default=func.now())
    answered_at = Column(DateTime)

    # Relationships (using string references to avoid circular imports)
    session = relationship("InterviewSession", back_populates="answers")
