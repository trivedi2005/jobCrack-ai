from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate
from typing import Optional, List, Dict


class CompanyService:
    def __init__(self, db: Session):
        self.db = db

    def create_company(self, company_data: CompanyCreate) -> Company:
        """Create a new company."""
        # Check if company already exists
        existing = self.db.query(Company).filter(
            Company.name == company_data.name
        ).first()
        if existing:
            raise ValueError("Company with this name already exists")
        
        company = Company(**company_data.model_dump())
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company

    def get_company(self, company_id: int) -> Optional[Company]:
        """Get company by ID."""
        return self.db.query(Company).filter(Company.id == company_id).first()

    def get_companies(
        self, 
        search: Optional[str] = None,
        industry: Optional[str] = None,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Company]:
        """Get companies with optional filters."""
        query = self.db.query(Company)
        
        if search:
            query = query.filter(
                or_(
                    Company.name.ilike(f"%{search}%"),
                    Company.industry.ilike(f"%{search}%")
                )
            )
        
        if industry:
            query = query.filter(Company.industry == industry)
        
        return query.offset(skip).limit(limit).all()

    def update_company(self, company_id: int, company_data: CompanyUpdate) -> Optional[Company]:
        """Update company."""
        company = self.get_company(company_id)
        if not company:
            return None
        
        for field, value in company_data.model_dump(exclude_unset=True).items():
            setattr(company, field, value)
        
        self.db.commit()
        self.db.refresh(company)
        return company

    def delete_company(self, company_id: int) -> bool:
        """Delete company."""
        company = self.get_company(company_id)
        if not company:
            return False
        
        self.db.delete(company)
        self.db.commit()
        return True

    def get_company_stats(self, company_id: int) -> dict:
        """Get company statistics."""
        company = self.get_company(company_id)
        if not company:
            return {}
        
        jobs_count = self.db.query(Job).filter(Job.company_id == company_id).count()
        
        return {
            "current_jobs_count": jobs_count,
            "interview_questions_count": 0,  # TODO: Implement when interview questions are added
            "coding_questions_count": 0,  # TODO: Implement when coding questions are added
        }
