from sqlalchemy.orm import Session
from app.models.resume import Resume, ResumeVersion, ResumeAnalysis
from app.models.user import User
from app.schemas.resume import ResumeCreate, ResumeAnalysisRequest
from typing import Optional, List
import os
import uuid
from datetime import datetime


class ResumeService:
    def __init__(self, db: Session):
        self.db = db
        self.upload_dir = "uploads"

    def _ensure_upload_dir(self):
        """Ensure upload directory exists."""
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

    def _generate_filename(self, original_filename: str) -> str:
        """Generate unique filename."""
        ext = os.path.splitext(original_filename)[1]
        return f"resume_{uuid.uuid4().hex}{ext}"

    def upload_resume(self, user_id: int, file_data: bytes, filename: str, file_type: str) -> Resume:
        """Upload and create resume record."""
        self._ensure_upload_dir()
        
        # Generate unique filename
        new_filename = self._generate_filename(filename)
        file_path = os.path.join(self.upload_dir, new_filename)
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        # Set other resumes as not current
        self.db.query(Resume).filter(Resume.user_id == user_id).update({"is_current": False})
        
        # Create resume record
        resume = Resume(
            user_id=user_id,
            original_filename=filename,
            file_path=file_path,
            file_size=len(file_data),
            file_type=file_type,
            is_current=True,
            version=1
        )
        
        self.db.add(resume)
        self.db.commit()
        self.db.refresh(resume)
        
        return resume

    def get_user_resumes(self, user_id: int) -> List[Resume]:
        """Get all resumes for a user."""
        return self.db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.created_at.desc()).all()

    def get_resume(self, resume_id: int) -> Optional[Resume]:
        """Get resume by ID."""
        return self.db.query(Resume).filter(Resume.id == resume_id).first()

    def get_current_resume(self, user_id: int) -> Optional[Resume]:
        """Get current resume for user."""
        return self.db.query(Resume).filter(
            Resume.user_id == user_id,
            Resume.is_current == True
        ).first()

    def parse_resume(self, resume_id: int) -> dict:
        """Parse resume and extract information."""
        resume = self.get_resume(resume_id)
        if not resume:
            raise ValueError("Resume not found")
        
        # TODO: Implement actual resume parsing
        # For now, return mock parsed data
        parsed_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+91 9876543210",
            "skills": ["Java", "Python", "React", "SQL"],
            "experience": [
                {
                    "company": "Previous Company",
                    "role": "Software Developer",
                    "duration": "2 years"
                }
            ],
            "education": [
                {
                    "degree": "B.Tech",
                    "institution": "IIT Bangalore",
                    "year": "2022"
                }
            ]
        }
        
        # Update resume with parsed data
        resume.parsed_data = parsed_data
        self.db.commit()
        self.db.refresh(resume)
        
        return parsed_data

    def analyze_resume(self, resume_id: int, job_id: Optional[int] = None) -> ResumeAnalysis:
        """Analyze resume and generate ATS scores."""
        resume = self.get_resume(resume_id)
        if not resume:
            raise ValueError("Resume not found")
        
        # TODO: Implement actual ATS analysis
        # For now, return mock analysis
        analysis = ResumeAnalysis(
            resume_id=resume_id,
            job_id=job_id,
            keyword_score=89.0,
            structure_score=92.0,
            formatting_score=85.0,
            overall_score=88.0,
            matched_keywords=["Java", "Spring Boot", "React", "SQL"],
            missing_keywords=["AWS", "Docker", "Kubernetes"],
            suggested_improvements=[
                "Add AWS certification details",
                "Include more project metrics",
                "Improve formatting consistency"
            ],
            skill_gaps=[
                {
                    "skill": "AWS",
                    "importance": "high",
                    "suggested_resources": ["AWS Certification Course"]
                }
            ],
            job_match_score=78.0 if job_id else None,
            experience_match={
                "matched": True,
                "details": "Experience aligns with job requirements"
            } if job_id else None,
            education_match={
                "matched": True,
                "details": "Education meets requirements"
            } if job_id else None
        )
        
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        
        return analysis

    def create_resume_version(self, resume_id: int, version_name: str, content: str, job_id: Optional[int] = None) -> ResumeVersion:
        """Create a new version of resume."""
        resume = self.get_resume(resume_id)
        if not resume:
            raise ValueError("Resume not found")
        
        resume_version = ResumeVersion(
            resume_id=resume_id,
            job_id=job_id,
            version_name=version_name,
            content=content,
            is_ai_tailored=job_id is not None
        )
        
        self.db.add(resume_version)
        self.db.commit()
        self.db.refresh(resume_version)
        
        return resume_version

    def get_resume_versions(self, resume_id: int) -> List[ResumeVersion]:
        """Get all versions of a resume."""
        return self.db.query(ResumeVersion).filter(
            ResumeVersion.resume_id == resume_id
        ).order_by(ResumeVersion.created_at.desc()).all()

    def delete_resume(self, resume_id: int) -> bool:
        """Delete resume."""
        resume = self.get_resume(resume_id)
        if not resume:
            return False
        
        # Delete file
        if os.path.exists(resume.file_path):
            os.remove(resume.file_path)
        
        self.db.delete(resume)
        self.db.commit()
        return True

    def set_current_resume(self, user_id: int, resume_id: int) -> bool:
        """Set resume as current for user."""
        resume = self.get_resume(resume_id)
        if not resume or resume.user_id != user_id:
            return False
        
        # Set all user's resumes as not current
        self.db.query(Resume).filter(Resume.user_id == user_id).update({"is_current": False})
        
        # Set this resume as current
        resume.is_current = True
        self.db.commit()
        
        return True
