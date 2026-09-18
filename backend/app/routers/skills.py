from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.schemas.profile import SkillCreate, SkillResponse
from app.services.skill_service import SkillService

router = APIRouter()


@router.get("/", response_model=list[SkillResponse])
async def get_skills(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all skills with optional filters."""
    skill_service = SkillService(db)
    skills = skill_service.get_skills(search=search, category=category, skip=skip, limit=limit)
    return skills


@router.get("/popular", response_model=list[SkillResponse])
async def get_popular_skills(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get popular skills."""
    skill_service = SkillService(db)
    skills = skill_service.get_popular_skills(limit=limit)
    return skills


@router.get("/{skill_id}", response_model=SkillResponse)
async def get_skill(skill_id: int, db: Session = Depends(get_db)):
    """Get skill by ID."""
    skill_service = SkillService(db)
    skill = skill_service.get_skill(skill_id)
    
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    return skill


@router.post("/", response_model=SkillResponse)
async def create_skill(
    skill_data: SkillCreate,
    db: Session = Depends(get_db)
):
    """Create a new skill."""
    skill_service = SkillService(db)
    skill = skill_service.create_skill(skill_data)
    return skill
