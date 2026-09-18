from sqlalchemy.orm import Session
from app.models.skill import Skill
from app.schemas.profile import SkillCreate
from typing import Optional, List


class SkillService:
    def __init__(self, db: Session):
        self.db = db

    def create_skill(self, skill_data: SkillCreate) -> Skill:
        """Create a new skill."""
        # Check if skill already exists
        existing = self.db.query(Skill).filter(
            Skill.name == skill_data.name
        ).first()
        if existing:
            return existing
        
        skill = Skill(**skill_data.model_dump())
        self.db.add(skill)
        self.db.commit()
        self.db.refresh(skill)
        return skill

    def get_skill(self, skill_id: int) -> Optional[Skill]:
        """Get skill by ID."""
        return self.db.query(Skill).filter(Skill.id == skill_id).first()

    def get_skills(
        self, 
        search: Optional[str] = None,
        category: Optional[str] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Skill]:
        """Get skills with optional filters."""
        query = self.db.query(Skill)
        
        if search:
            query = query.filter(Skill.name.ilike(f"%{search}%"))
        
        if category:
            query = query.filter(Skill.category == category)
        
        return query.offset(skip).limit(limit).all()

    def get_or_create_skill(self, name: str, category: Optional[str] = None) -> Skill:
        """Get existing skill or create new one."""
        skill = self.db.query(Skill).filter(Skill.name == name).first()
        if skill:
            return skill
        
        skill = Skill(name=name, category=category)
        self.db.add(skill)
        self.db.commit()
        self.db.refresh(skill)
        return skill

    def get_popular_skills(self, limit: int = 20) -> List[Skill]:
        """Get popular skills (simplified - returns most recently created)."""
        return self.db.query(Skill).order_by(Skill.created_at.desc()).limit(limit).all()
