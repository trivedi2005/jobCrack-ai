from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.middleware.auth import get_current_user
from app.models.preparation import PreparationPlan, PreparationTask
from app.models.user import User

router = APIRouter()


class PreparationRequest(BaseModel):
    job_id: Optional[int] = None
    company_id: Optional[int] = None
    role: str = Field(default="Software Engineer", min_length=2)
    duration_days: int = Field(default=7, ge=3, le=30)


class TaskUpdate(BaseModel):
    status: str = Field(pattern="^(pending|in_progress|completed)$")


def serialize_plan(plan: PreparationPlan) -> dict:
    tasks = sorted(plan.tasks, key=lambda task: task.day_number or 0)
    return {
        "id": plan.id,
        "title": plan.plan_name,
        "duration_days": plan.duration_days,
        "progress_percentage": plan.progress_percentage or 0,
        "tasks": [
            {
                "id": task.id,
                "day": task.day_number,
                "title": task.title,
                "description": task.description,
                "topic": task.topic,
                "status": task.status,
                "estimated_hours": task.estimated_hours,
            }
            for task in tasks
        ],
    }


@router.get("/current")
async def current_preparation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    plan = db.query(PreparationPlan).filter(
        PreparationPlan.user_id == current_user.id,
        PreparationPlan.is_active == True,
    ).order_by(PreparationPlan.created_at.desc()).first()
    return serialize_plan(plan) if plan else {"plan": None}


@router.post("/generate")
async def generate_preparation(
    request: PreparationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db.query(PreparationPlan).filter(
        PreparationPlan.user_id == current_user.id,
        PreparationPlan.is_active == True,
    ).update({"is_active": False})

    topics = [
        ("Core fundamentals", "Review language fundamentals, OOP, and problem-solving patterns."),
        ("Data structures", "Practice arrays, strings, hash maps, trees, and complexity analysis."),
        ("Databases", "Revise SQL joins, indexing, transactions, and database design."),
        ("System design", "Prepare scalable service design, APIs, caching, and trade-offs."),
        ("Project storytelling", "Build concise STAR stories around your strongest projects."),
        ("Behavioral interview", "Practice leadership, conflict, failure, and motivation questions."),
        ("Mock interview", "Run a timed technical and behavioral interview and review gaps."),
    ]
    topics = (topics * ((request.duration_days + len(topics) - 1) // len(topics)))[:request.duration_days]
    plan = PreparationPlan(
        user_id=current_user.id,
        company_id=request.company_id,
        job_id=request.job_id,
        plan_name=f"{request.role} interview preparation",
        plan_type="interview",
        duration_days=request.duration_days,
        total_tasks=request.duration_days,
        is_active=True,
        start_date=datetime.now(timezone.utc),
        end_date=datetime.now(timezone.utc) + timedelta(days=request.duration_days),
    )
    db.add(plan)
    db.flush()
    for day, (title, description) in enumerate(topics, start=1):
        db.add(PreparationTask(
            plan_id=plan.id,
            title=title,
            description=description,
            topic=title,
            task_type="interview",
            status="in_progress" if day == 1 else "pending",
            day_number=day,
            estimated_hours=2,
        ))
    db.commit()
    db.refresh(plan)
    return serialize_plan(plan)


@router.patch("/tasks/{task_id}")
async def update_preparation_task(
    task_id: int,
    request: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    task = db.query(PreparationTask).join(PreparationPlan).filter(
        PreparationTask.id == task_id,
        PreparationPlan.user_id == current_user.id,
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Preparation task not found")
    task.status = request.status
    task.completed_at = datetime.now(timezone.utc) if request.status == "completed" else None
    plan = task.plan
    completed = sum(item.status == "completed" for item in plan.tasks)
    plan.tasks_completed = completed
    plan.progress_percentage = round(completed / max(plan.total_tasks, 1) * 100, 1)
    db.commit()
    return serialize_plan(plan)
