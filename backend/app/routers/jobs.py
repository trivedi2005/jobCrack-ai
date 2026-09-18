from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.schemas.job import JobCreate, JobUpdate, JobResponse, JobListResponse, JobFilter
from app.services.job_service import JobService

router = APIRouter()


@router.get("/", response_model=dict)
async def get_jobs(
    search: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    job_type: Optional[str] = Query(None),
    work_mode: Optional[str] = Query(None),
    experience_level: Optional[str] = Query(None),
    salary_min: Optional[int] = Query(None),
    salary_max: Optional[int] = Query(None),
    company_id: Optional[int] = Query(None),
    sort_by: Optional[str] = Query("relevance"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all jobs with filters and pagination."""
    job_service = JobService(db)
    
    filters = JobFilter(
        search=search,
        location=location,
        job_type=job_type,
        work_mode=work_mode,
        experience_level=experience_level,
        salary_min=salary_min,
        salary_max=salary_max,
        company_id=company_id,
        sort_by=sort_by
    )
    
    jobs, total = job_service.get_jobs(filters=filters, skip=skip, limit=limit)
    
    # Convert to list response format
    job_list = []
    for job in jobs:
        job_dict = {
            "id": job.id,
            "title": job.title,
            "company_name": job.company.name if job.company else None,
            "company_logo": job.company.logo_url if job.company else None,
            "location": job.location,
            "job_type": job.job_type,
            "work_mode": job.work_mode,
            "experience_level": job.experience_level,
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "salary_currency": job.salary_currency,
            "posted_date": job.posted_date,
            "match_percentage": None  # TODO: Calculate when user context is available
        }
        job_list.append(JobListResponse(**job_dict))
    
    return {
        "jobs": job_list,
        "total": total,
        "page": skip // limit + 1,
        "per_page": limit
    }


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get job details."""
    job_service = JobService(db)
    job = job_service.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job


@router.post("/", response_model=JobResponse)
async def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db)
):
    """Create a new job."""
    job_service = JobService(db)
    try:
        job = job_service.create_job(job_data)
        return job
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db)
):
    """Update job."""
    job_service = JobService(db)
    job = job_service.update_job(job_id, job_data)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job


@router.delete("/{job_id}")
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    """Delete job (soft delete)."""
    job_service = JobService(db)
    success = job_service.delete_job(job_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {"message": "Job deleted successfully"}


@router.get("/{job_id}/skills")
async def get_job_skills(job_id: int, db: Session = Depends(get_db)):
    """Get skills for a specific job."""
    job_service = JobService(db)
    skills = job_service.get_job_skills(job_id)
    return {"skills": skills}


@router.get("/location/{location}")
async def search_jobs_by_location(
    location: str,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Search jobs by location."""
    job_service = JobService(db)
    jobs = job_service.search_jobs_by_location(location, limit=limit)
    
    job_list = []
    for job in jobs:
        job_dict = {
            "id": job.id,
            "title": job.title,
            "company_name": job.company.name if job.company else None,
            "location": job.location,
            "posted_date": job.posted_date
        }
        job_list.append(job_dict)
    
    return {"jobs": job_list, "total": len(job_list)}
