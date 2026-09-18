from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models.job import Job, JobSkill
from app.models.company import Company
from app.models.skill import Skill
from app.schemas.job import JobCreate, JobUpdate, JobFilter
from typing import Optional, List


class JobService:
    def __init__(self, db: Session):
        self.db = db

    def create_job(self, job_data: JobCreate) -> Job:
        """Create a new job."""
        # Verify company exists
        company = self.db.query(Company).filter(Company.id == job_data.company_id).first()
        if not company:
            raise ValueError("Company not found")
        
        job = Job(**job_data.model_dump(exclude={'required_skills', 'preferred_skills'}))
        self.db.add(job)
        self.db.flush()  # Get job ID before adding skills
        
        # Add required skills
        if job_data.required_skills:
            for skill_id in job_data.required_skills:
                skill = self.db.query(Skill).filter(Skill.id == skill_id).first()
                if skill:
                    job_skill = JobSkill(job_id=job.id, skill_id=skill_id, is_required=True)
                    self.db.add(job_skill)
        
        # Add preferred skills
        if job_data.preferred_skills:
            for skill_id in job_data.preferred_skills:
                skill = self.db.query(Skill).filter(Skill.id == skill_id).first()
                if skill:
                    job_skill = JobSkill(job_id=job.id, skill_id=skill_id, is_required=False)
                    self.db.add(job_skill)
        
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_job(self, job_id: int) -> Optional[Job]:
        """Get job by ID with company info."""
        return self.db.query(Job).filter(Job.id == job_id).first()

    def get_jobs(
        self, 
        filters: JobFilter,
        skip: int = 0, 
        limit: int = 20
    ) -> tuple[List[Job], int]:
        """Get jobs with filters and pagination."""
        query = self.db.query(Job)
        
        # Search filter
        if filters.search:
            search_term = f"%{filters.search}%"
            query = query.filter(
                or_(
                    Job.title.ilike(search_term),
                    Job.description.ilike(search_term)
                )
            )
        
        # Location filter
        if filters.location:
            query = query.filter(Job.location.ilike(f"%{filters.location}%"))
        
        # Job type filter
        if filters.job_type:
            query = query.filter(Job.job_type == filters.job_type)
        
        # Work mode filter
        if filters.work_mode:
            query = query.filter(Job.work_mode == filters.work_mode)
        
        # Experience level filter
        if filters.experience_level:
            query = query.filter(Job.experience_level == filters.experience_level)
        
        # Salary range filter
        if filters.salary_min:
            query = query.filter(Job.salary_min >= filters.salary_min)
        if filters.salary_max:
            query = query.filter(Job.salary_max <= filters.salary_max)
        
        # Company filter
        if filters.company_id:
            query = query.filter(Job.company_id == filters.company_id)
        
        # Active jobs only
        query = query.filter(Job.is_active == True)
        
        # Get total count
        total = query.count()
        
        # Sorting
        if filters.sort_by == "newest":
            query = query.order_by(Job.posted_date.desc())
        elif filters.sort_by == "match":
            # TODO: Implement match-based sorting when user context is available
            query = query.order_by(Job.posted_date.desc())
        else:  # relevance (default)
            query = query.order_by(Job.posted_date.desc())
        
        # Pagination
        jobs = query.offset(skip).limit(limit).all()
        
        return jobs, total

    def update_job(self, job_id: int, job_data: JobUpdate) -> Optional[Job]:
        """Update job."""
        job = self.get_job(job_id)
        if not job:
            return None
        
        for field, value in job_data.model_dump(exclude_unset=True).items():
            if field not in ['required_skills', 'preferred_skills']:
                setattr(job, field, value)
        
        # Update skills if provided
        if job_data.required_skills is not None or job_data.preferred_skills is not None:
            # Remove existing skills
            self.db.query(JobSkill).filter(JobSkill.job_id == job_id).delete()
            
            # Add new required skills
            if job_data.required_skills:
                for skill_id in job_data.required_skills:
                    skill = self.db.query(Skill).filter(Skill.id == skill_id).first()
                    if skill:
                        job_skill = JobSkill(job_id=job.id, skill_id=skill_id, is_required=True)
                        self.db.add(job_skill)
            
            # Add new preferred skills
            if job_data.preferred_skills:
                for skill_id in job_data.preferred_skills:
                    skill = self.db.query(Skill).filter(Skill.id == skill_id).first()
                    if skill:
                        job_skill = JobSkill(job_id=job.id, skill_id=skill_id, is_required=False)
                        self.db.add(job_skill)
        
        self.db.commit()
        self.db.refresh(job)
        return job

    def delete_job(self, job_id: int) -> bool:
        """Delete job (soft delete by setting is_active to False)."""
        job = self.get_job(job_id)
        if not job:
            return False
        
        job.is_active = False
        self.db.commit()
        return True

    def get_job_skills(self, job_id: int) -> List[dict]:
        """Get skills for a job."""
        job_skills = self.db.query(JobSkill).filter(JobSkill.job_id == job_id).all()
        
        result = []
        for js in job_skills:
            skill = self.db.query(Skill).filter(Skill.id == js.skill_id).first()
            if skill:
                result.append({
                    "id": skill.id,
                    "name": skill.name,
                    "category": skill.category,
                    "is_required": js.is_required
                })
        
        return result

    def search_jobs_by_location(self, location: str, limit: int = 20) -> List[Job]:
        """Search jobs by location."""
        return self.db.query(Job).filter(
            and_(
                Job.location.ilike(f"%{location}%"),
                Job.is_active == True
            )
        ).order_by(Job.posted_date.desc()).limit(limit).all()
