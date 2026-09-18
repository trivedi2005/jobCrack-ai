from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.resume import ResumeAnalysisRequest, ResumeAnalysisResponse, ResumeResponse, ResumeRoleRequest, ResumeVersionResponse
from app.services.resume_service import ResumeService

router = APIRouter()


@router.get("/", response_model=list[ResumeResponse])
async def list_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ResumeService(db).get_user_resumes(current_user.id)


@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    extension = (file.filename or "").lower().rsplit(".", 1)[-1]
    if extension not in {"pdf", "docx"}:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX resumes are supported")

    file_data = await file.read()
    if len(file_data) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Resume must be 10 MB or smaller")

    return ResumeService(db).upload_resume(
        current_user.id,
        file_data,
        file.filename or "resume",
        extension,
    )


@router.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    request: ResumeAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ResumeService(db)
    resume = service.get_resume(request.resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")

    try:
        return service.analyze_resume(request.resume_id, request.job_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.post("/tailor", response_model=ResumeVersionResponse)
async def tailor_resume(
    request: ResumeRoleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ResumeService(db)
    resume = service.get_resume(request.resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    content = (
        f"ATS-tailored resume for {request.target_role}\n\n"
        "Use measurable achievements, role-specific keywords, and clear sections. "
        "Review and edit this version before submitting it to an employer."
    )
    return service.create_resume_version(
        request.resume_id,
        f"ATS version - {request.target_role}",
        content,
    )
