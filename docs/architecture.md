# JobCrack AI - Architecture Documentation

## System Architecture

JobCrack AI follows a monorepo architecture with separate frontend and backend applications, connected through REST APIs.

### Architecture Overview

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   Frontend      │         │   Backend       │         │   Database      │
│   (Next.js)     │◄────────┤   (FastAPI)     │◄────────┤   PostgreSQL     │
│                 │  HTTP   │                 │  SQL    │   + pgvector    │
│   React + TS    │         │   Python        │         │                 │
│   Tailwind      │         │   SQLAlchemy    │         │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘
                                   │
                                   │
                                   ▼
                            ┌─────────────────┐
                            │   Redis         │
                            │   (Cache/Queue) │
                            └─────────────────┘
                                   │
                                   │
                                   ▼
                            ┌─────────────────┐
                            │   AI Services   │
                            │   (Groq/LLM)    │
                            │   RAG Pipeline  │
                            └─────────────────┘
```

## Technology Stack

### Frontend
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui (custom built)
- **State Management**: React Hooks + TanStack Query
- **Form Handling**: React Hook Form + Zod validation
- **HTTP Client**: Axios with interceptors
- **Icons**: Lucide React
- **Charts**: Recharts

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **ORM**: SQLAlchemy 2.0
- **Database**: PostgreSQL with pgvector
- **Migration**: Alembic
- **Authentication**: JWT (access + refresh tokens)
- **Password Hashing**: bcrypt
- **API Documentation**: Swagger/OpenAPI (built-in)
- **CORS**: Configured for frontend integration

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Process Management**: Uvicorn
- **Environment**: dotenv
- **Version Control**: Git

### AI/ML
- **LLM Provider**: Groq (configurable)
- **Embeddings**: Configurable embedding models
- **RAG**: Custom RAG pipeline with pgvector
- **Document Processing**: PyPDF2, python-docx

## Project Structure

### Backend Structure
```
backend/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── config.py          # Configuration and settings
│   │   ├── security.py       # JWT, password hashing
│   │   └── database.py       # Database connection and session
│   ├── models/                # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── profile.py
│   │   ├── company.py
│   │   ├── job.py
│   │   ├── resume.py
│   │   ├── interview.py
│   │   ├── matching.py
│   │   ├── application.py
│   │   ├── preparation.py
│   │   ├── notification.py
│   │   └── admin.py
│   ├── schemas/               # Pydantic schemas for validation
│   │   ├── user.py
│   │   ├── profile.py
│   │   ├── job.py
│   │   ├── company.py
│   │   ├── resume.py
│   │   ├── matching.py
│   │   ├── preparation.py
│   │   └── application.py
│   ├── routers/               # API route handlers
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── jobs.py
│   │   ├── companies.py
│   │   ├── resumes.py
│   │   ├── matching.py
│   │   ├── preparation.py
│   │   ├── coding.py
│   │   ├── interviews.py
│   │   ├── applications.py
│   │   ├── notifications.py
│   │   └── ai.py
│   ├── services/              # Business logic layer
│   │   ├── auth_service.py
│   │   ├── profile_service.py
│   │   ├── job_service.py
│   │   ├── resume_service.py
│   │   ├── matching_service.py
│   │   ├── interview_service.py
│   │   ├── preparation_service.py
│   │   ├── ai_service.py
│   │   └── rag_service.py
│   ├── repositories/          # Data access layer
│   ├── middleware/            # Custom middleware
│   │   └── auth.py
│   └── utils/                # Utility functions
├── alembic/                   # Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── tests/                     # Test suite
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
└── alembic.ini               # Alembic configuration
```

### Frontend Structure
```
frontend/
├── app/
│   ├── layout.tsx            # Root layout
│   ├── page.tsx              # Landing page
│   ├── globals.css           # Global styles
│   ├── login/                # Login page
│   ├── register/             # Registration page
│   ├── dashboard/            # Dashboard
│   ├── jobs/                 # Job discovery
│   ├── companies/            # Company profiles
│   ├── preparation/          # Preparation plans
│   ├── coding/               # Coding practice
│   ├── interviews/           # Mock interviews
│   ├── resume/               # Resume studio
│   ├── applications/         # Application tracker
│   ├── profile/              # User profile
│   └── settings/             # Settings
├── components/
│   ├── ui/                   # UI components (Button, etc.)
│   ├── layout/               # Layout components
│   ├── dashboard/            # Dashboard components
│   ├── jobs/                 # Job-related components
│   ├── resume/               # Resume components
│   ├── interview/            # Interview components
│   └── coding/               # Coding components
├── lib/
│   ├── api.ts                # Axios client with interceptors
│   ├── auth.ts               # Authentication utilities
│   └── utils.ts              # Utility functions
├── hooks/                    # Custom React hooks
├── types/                    # TypeScript type definitions
├── package.json              # Node dependencies
├── tsconfig.json             # TypeScript configuration
├── tailwind.config.ts        # Tailwind configuration
├── next.config.js            # Next.js configuration
└── Dockerfile                # Docker configuration
```

## Database Schema

### Core Tables

**Users**
- `id` (PK)
- `email` (unique)
- `hashed_password`
- `role` (candidate/recruiter/admin)
- `is_active`, `is_verified`
- `created_at`, `updated_at`

**Profiles**
- `id` (PK)
- `user_id` (FK)
- Personal information (name, phone, location)
- Career preferences (roles, experience, salary)
- Profile completeness score

**Skills**
- `id` (PK)
- `name`, `category`
- User skills junction table

**Companies**
- `id` (PK)
- `name`, `logo`, `website`
- Industry, description, locations
- Verification status

**Jobs**
- `id` (PK)
- `company_id` (FK)
- Title, description, requirements
- Location, job type, work mode
- Salary range, experience level
- Skills required/preferred
- Source, verification status

**Resumes**
- `id` (PK)
- `user_id` (FK)
- File information
- Parsed content
- Version tracking

**Resume Analysis**
- ATS scores (keywords, structure, formatting)
- Match analysis
- Improvement suggestions

**Job Matches**
- `user_id`, `job_id`
- Match scores (overall, skills, experience, etc.)
- Matched/missing skills
- Preparation suggestions

**Interview Questions**
- Company, role, round, topic
- Question, answer, explanation
- Difficulty, verification status

**Interview Sessions**
- User, job, company
- Session details, AI feedback
- Score, technical/communication feedback

**Applications**
- User, job, company
- Status tracking
- Timeline events

**Preparation Plans**
- User, company, job
- Plan details, progress
- Tasks with completion status

**Notifications**
- User, type, message
- Read status, delivery status

## API Design

### Authentication Flow
1. User registers → JWT tokens generated
2. Access token (30min) + Refresh token (7 days)
3. Token refresh on expiration
4. Protected routes require valid access token

### REST API Endpoints

**Authentication**
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Token refresh
- `POST /api/auth/logout` - User logout

**Users**
- `GET /api/users/me` - Get current user
- `PUT /api/users/me` - Update user
- `GET /api/users/me/profile` - Get profile
- `PUT /api/users/me/profile` - Update profile
- `POST /api/users/me/education` - Add education
- `POST /api/users/me/skills` - Add skill

**Jobs**
- `GET /api/jobs` - List jobs with filters
- `GET /api/jobs/{id}` - Get job details
- `POST /api/jobs/{id}/match` - Get job match analysis

**Companies**
- `GET /api/companies` - List companies
- `GET /api/companies/{id}` - Get company details
- `GET /api/companies/{id}/questions` - Get interview questions

**Resumes**
- `POST /api/resumes/upload` - Upload resume
- `POST /api/resumes/analyze` - Analyze resume
- `POST /api/resumes/tailor` - Tailor resume for job

**Matching**
- `POST /api/matching/jobs/{id}/match` - Match user with job

**Preparation**
- `POST /api/preparation/generate` - Generate preparation plan
- `GET /api/preparation/{id}` - Get preparation plan

**Applications**
- `GET /api/applications` - List applications
- `POST /api/applications` - Create application
- `PUT /api/applications/{id}` - Update application

**AI**
- `POST /api/ai/chat` - AI Career Copilot chat

## Security Considerations

### Authentication
- JWT with short-lived access tokens (30 min)
- Refresh tokens with longer expiry (7 days)
- Password hashing with bcrypt
- Token refresh mechanism with automatic retry

### Data Protection
- SQL injection prevention via ORM
- XSS-safe rendering in frontend
- Input validation with Pydantic/Zod
- File upload validation (type, size)
- Secure file storage for resumes

### API Security
- CORS configuration
- Rate limiting (configurable)
- Role-based authorization
- Protected routes with middleware

### Environment Variables
- Never commit `.env` files
- Use `.env.example` for documentation
- Separate development/production configs
- Secure credential management

## Performance Considerations

### Database
- Connection pooling
- Indexed columns (email, job title, location)
- Query optimization with eager loading
- Database health checks

### Caching
- Redis for session data
- API response caching where appropriate
- Frontend caching with TanStack Query

### Frontend
- Code splitting with Next.js
- Image optimization
- Lazy loading components
- Debounced search inputs

## Scalability

### Horizontal Scaling
- Stateless API design
- External session storage (Redis)
- Load balancer ready
- Container orchestration ready

### Database Scaling
- Connection pooling
- Read replicas (future)
- Database indexing strategy
- Query optimization

### Future Enhancements
- Microservices architecture option
- Message queue for background jobs
- CDN for static assets
- Monitoring and logging (Prometheus, Grafana)

## Development Workflow

### Local Development
1. Start PostgreSQL and Redis with Docker Compose
2. Run database migrations with Alembic
3. Start FastAPI backend with `uvicorn`
4. Start Next.js frontend with `npm run dev`
5. Access application at `http://localhost:3000`

### Testing
- Backend: pytest with async support
- Frontend: Jest + React Testing Library
- API testing: integration tests
- E2E testing: Playwright (future)

### Deployment
- Docker containers for both services
- Environment-specific configurations
- Database migrations on deploy
- Health checks and monitoring
