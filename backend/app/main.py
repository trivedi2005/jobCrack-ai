import logging

from fastapi import FastAPI
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.routers import auth, users, jobs, companies, resumes, matching, preparation, coding, interviews, applications, notifications, ai, skills, network

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

# Initialize FastAPI app
app = FastAPI(
    title="JobCrack AI API",
    description="AI-powered career platform API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)


@app.on_event("startup")
def initialize_database() -> None:
    """Create missing tables without preventing the API from starting."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables are ready")
    except Exception:
        logger.exception("Database initialization failed; database-backed endpoints may be unavailable")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SecurityHeadersMiddleware)


@app.get("/")
def root():
    return {
        "name": "JobCrack AI API",
        "status": "running",
        "docs": "/api/docs",
        "health": "/health",
    }


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception:
        return {
            "status": "degraded",
            "database": "unavailable",
            "version": "1.0.0"
        }

    return {
        "status": "healthy",
        "database": "connected",
        "version": "1.0.0"
    }

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(companies.router, prefix="/api/companies", tags=["Companies"])
app.include_router(skills.router, prefix="/api/skills", tags=["Skills"])
app.include_router(resumes.router, prefix="/api/resumes", tags=["Resumes"])
app.include_router(matching.router, prefix="/api/matching", tags=["Matching"])
app.include_router(preparation.router, prefix="/api/preparation", tags=["Preparation"])
app.include_router(coding.router, prefix="/api/coding", tags=["Coding"])
app.include_router(interviews.router, prefix="/api/interviews", tags=["Interviews"])
app.include_router(applications.router, prefix="/api/applications", tags=["Applications"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])
app.include_router(network.router, prefix="/api/network", tags=["Network"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
