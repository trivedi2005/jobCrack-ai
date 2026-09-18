from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class ReportStatus(str, enum.Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    reporter_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Report Details
    report_type = Column(String)  # job, company, question, content, user
    entity_type = Column(String)
    entity_id = Column(Integer)
    reason = Column(String)
    description = Column(Text)
    
    # Status
    status = Column(Enum(ReportStatus), default=ReportStatus.PENDING)
    reviewed_by = Column(Integer, ForeignKey("users.id"))
    review_notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class AdminAction(Base):
    __tablename__ = "admin_actions"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Action Details
    action_type = Column(String)  # create, update, delete, verify, reject
    entity_type = Column(String)  # job, company, question, user
    entity_id = Column(Integer)
    changes = Column(JSON)  # Description of changes made
    
    # Context
    reason = Column(Text)
    ip_address = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
