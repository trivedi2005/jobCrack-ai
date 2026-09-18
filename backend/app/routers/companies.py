from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse, CompanyDetailResponse
from app.services.company_service import CompanyService

router = APIRouter()


@router.get("/", response_model=list[CompanyResponse])
async def get_companies(
    search: Optional[str] = Query(None),
    industry: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all companies with optional filters."""
    company_service = CompanyService(db)
    companies = company_service.get_companies(search=search, industry=industry, skip=skip, limit=limit)
    return companies


@router.get("/{company_id}", response_model=CompanyDetailResponse)
async def get_company(company_id: int, db: Session = Depends(get_db)):
    """Get company details with statistics."""
    company_service = CompanyService(db)
    company = company_service.get_company(company_id)
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    stats = company_service.get_company_stats(company_id)
    
    # Convert to response model with stats
    company_dict = {
        **company.__dict__,
        **stats
    }
    
    return CompanyDetailResponse(**company_dict)


@router.post("/", response_model=CompanyResponse)
async def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db)
):
    """Create a new company."""
    company_service = CompanyService(db)
    try:
        company = company_service.create_company(company_data)
        return company
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db)
):
    """Update company."""
    company_service = CompanyService(db)
    company = company_service.update_company(company_id, company_data)
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return company


@router.delete("/{company_id}")
async def delete_company(company_id: int, db: Session = Depends(get_db)):
    """Delete company."""
    company_service = CompanyService(db)
    success = company_service.delete_company(company_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return {"message": "Company deleted successfully"}
