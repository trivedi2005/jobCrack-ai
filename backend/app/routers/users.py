from fastapi import APIRouter, Depends, Response
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.middleware.auth import get_current_active_user
from app.models.user import User
from app.schemas.user import UserResponse
from app.schemas.profile import (
    ProfileResponse, ProfileUpdate, 
    EducationCreate, EducationResponse,
    UserSkillCreate, UserSkillResponse
)
from app.services.profile_service import ProfileService
from app.models.application import Application
from app.models.interview import InterviewSession
from app.models.resume import Resume, ResumeAnalysis
from app.models.preparation import PreparationPlan, PreparationTask

router = APIRouter()


@router.get("/me/dashboard-summary")
async def get_dashboard_summary(
    response: Response,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    resume_count = db.query(func.count(Resume.id)).filter(Resume.user_id == current_user.id).scalar() or 0
    application_count = db.query(func.count(Application.id)).filter(Application.user_id == current_user.id).scalar() or 0
    interview_count = db.query(func.count(InterviewSession.id)).filter(InterviewSession.user_id == current_user.id).scalar() or 0
    latest_analysis = db.query(ResumeAnalysis).join(Resume).filter(
        Resume.user_id == current_user.id,
    ).order_by(ResumeAnalysis.created_at.desc()).first()
    active_plan = db.query(PreparationPlan).filter(
        PreparationPlan.user_id == current_user.id,
        PreparationPlan.is_active == True,
    ).order_by(PreparationPlan.created_at.desc()).first()
    tasks = []
    plan_progress = 0
    if active_plan:
        plan_progress = active_plan.progress_percentage or 0
        tasks = [
            {
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "estimated_hours": task.estimated_hours,
            }
            for task in sorted(active_plan.tasks, key=lambda item: item.day_number or 0)
            if task.status != "completed"
        ][:4]

    readiness = 0
    if resume_count:
        ats_score = latest_analysis.overall_score if latest_analysis else 0
        readiness = round((ats_score * 0.7) + (plan_progress * 0.3))

    return {
        "career_readiness": readiness,
        "applications": application_count,
        "interviews": interview_count,
        "practice_score": plan_progress,
        "resume_count": resume_count,
        "tasks": tasks,
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user profile."""
    return current_user


@router.get("/me/profile", response_model=ProfileResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's detailed profile."""
    profile_service = ProfileService(db)
    profile = profile_service.get_or_create_profile(current_user.id)
    return profile


@router.put("/me/profile", response_model=ProfileResponse)
async def update_user_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile."""
    profile_service = ProfileService(db)
    profile = profile_service.update_profile(current_user.id, profile_data)
    return profile


@router.post("/me/education", response_model=EducationResponse)
async def add_education(
    education_data: EducationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add education to user profile."""
    profile_service = ProfileService(db)
    education = profile_service.add_education(current_user.id, education_data)
    return education


@router.post("/me/skills", response_model=UserSkillResponse)
async def add_skill(
    skill_data: UserSkillCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add skill to user profile."""
    profile_service = ProfileService(db)
    user_skill = profile_service.add_skill(current_user.id, skill_data)
    return user_skill


@router.get("/me/completeness")
async def get_profile_completeness(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get profile completeness breakdown."""
    profile_service = ProfileService(db)
    completeness = profile_service.get_profile_completeness(current_user.id)
    return completeness
