from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class PreparationPlan(Base):
    __tablename__ = "preparation_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)
    
    plan_name = Column(String(255), nullable=True)
    plan_type = Column(String(50), nullable=True)
    duration_days = Column(Integer, nullable=True)
    
    progress_percentage = Column(Float, default=0.0)
    tasks_completed = Column(Integer, default=0)
    total_tasks = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="preparation_plans")
    tasks = relationship("PreparationTask", back_populates="plan", cascade="all, delete-orphan")


class PreparationTask(Base):
    __tablename__ = "preparation_tasks"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("preparation_plans.id", ondelete="CASCADE"), nullable=False)
    
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    task_type = Column(String(50), nullable=True)
    topic = Column(String(100), nullable=True)
    difficulty = Column(String(50), nullable=True)
    
    status = Column(String(50), default="pending")
    progress = Column(Float, default=0.0)
    day_number = Column(Integer, nullable=True)
    estimated_hours = Column(Integer, nullable=True)
    
    due_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    plan = relationship("PreparationPlan", back_populates="tasks")


class LearningTopic(Base):
    __tablename__ = "learning_topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TaskStatus(Base):
    __tablename__ = "task_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
