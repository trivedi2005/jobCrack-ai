from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.models.education import Education
from app.models.skill import Skill, UserSkill
from app.models.experience import Experience
from app.models.project import Project
from app.models.certification import Certification
from app.schemas.profile import (
    ProfileCreate, ProfileUpdate, 
    EducationCreate, 
    UserSkillCreate
)
from typing import Optional, List


class ProfileService:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create_profile(self, user_id: int) -> Profile:
        """Get existing profile or create new one."""
        profile = self.db.query(Profile).filter(Profile.user_id == user_id).first()
        if not profile:
            profile = Profile(user_id=user_id)
            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)
        return profile

    def update_profile(self, user_id: int, profile_data: ProfileUpdate) -> Profile:
        """Update user profile."""
        profile = self.get_or_create_profile(user_id)
        
        for field, value in profile_data.model_dump(exclude_unset=True).items():
            setattr(profile, field, value)
        
        # Calculate profile completeness
        profile.profile_completeness = self._calculate_completeness(profile)
        
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def _calculate_completeness(self, profile: Profile) -> float:
        """Calculate profile completeness percentage."""
        fields = [
            profile.full_name,
            profile.phone,
            profile.current_city,
            profile.preferred_locations,
            profile.target_roles,
            profile.preferred_work_mode,
            profile.job_type
        ]
        
        completed = sum(1 for field in fields if field is not None and field != [])
        return (completed / len(fields)) * 100

    def add_education(self, user_id: int, education_data: EducationCreate) -> Education:
        """Add education to profile."""
        profile = self.get_or_create_profile(user_id)
        
        education = Education(
            profile_id=profile.id,
            **education_data.model_dump()
        )
        
        self.db.add(education)
        self.db.commit()
        self.db.refresh(education)
        return education

    def add_skill(self, user_id: int, skill_data: UserSkillCreate) -> UserSkill:
        """Add skill to user profile."""
        profile = self.get_or_create_profile(user_id)
        
        # Check if skill exists
        skill = self.db.query(Skill).filter(Skill.id == skill_data.skill_id).first()
        if not skill:
            raise ValueError("Skill not found")
        
        # Check if user already has this skill
        existing = self.db.query(UserSkill).filter(
            UserSkill.profile_id == profile.id,
            UserSkill.skill_id == skill_data.skill_id
        ).first()
        
        if existing:
            # Update existing skill
            for field, value in skill_data.model_dump(exclude_unset=True).items():
                setattr(existing, field, value)
            self.db.commit()
            self.db.refresh(existing)
            return existing
        
        # Create new user skill
        user_skill = UserSkill(
            profile_id=profile.id,
            **skill_data.model_dump()
        )
        
        self.db.add(user_skill)
        self.db.commit()
        self.db.refresh(user_skill)
        return user_skill

    def get_profile_completeness(self, user_id: int) -> dict:
        """Get detailed profile completeness breakdown."""
        profile = self.get_or_create_profile(user_id)
        
        education_count = self.db.query(Education).filter(Education.profile_id == profile.id).count()
        skills_count = self.db.query(UserSkill).filter(UserSkill.profile_id == profile.id).count()
        experience_count = self.db.query(Experience).filter(Experience.profile_id == profile.id).count()
        projects_count = self.db.query(Project).filter(Project.profile_id == profile.id).count()
        certifications_count = self.db.query(Certification).filter(Certification.profile_id == profile.id).count()
        
        return {
            "overall": profile.profile_completeness,
            "personal": 100 if profile.full_name and profile.phone and profile.current_city else 0,
            "education": 100 if education_count > 0 else 0,
            "skills": min(100, skills_count * 10),  # Each skill adds 10%, max 100
            "experience": 100 if experience_count > 0 else 0,
            "projects": min(100, projects_count * 20),  # Each project adds 20%, max 100
            "certifications": min(100, certifications_count * 25)  # Each certification adds 25%, max 100
        }
