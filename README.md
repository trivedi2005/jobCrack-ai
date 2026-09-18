# JobCrack AI

Find the job. Prepare for the company. Crack the interview.

JobCrack AI is an AI-powered career platform for students, freshers, and early-career candidates.

## Product Overview

JobCrack AI brings the entire job-search and preparation workflow into one application:

**Discover Jobs → Analyze Fit → Optimize Resume → Prepare for Company → Practice Coding → Mock Interview → Apply → Track Application**

## Tech Stack

### Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- React Hook Form
- Zod
- TanStack Query
- Recharts
- Lucide icons

### Backend
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

### Database
- PostgreSQL
- pgvector (for vector search)

### Cache/Background Jobs
- Redis

### AI
- Groq-compatible LLM APIs
- Embeddings
- RAG
- Configurable LLM provider

### Infrastructure
- Docker
- Docker Compose

## Project Structure

```
jobcrack-ai/
├── frontend/          # Next.js application
├── backend/           # FastAPI application
├── infra/             # Docker and infrastructure configs
├── docs/              # Documentation
├── scripts/           # Utility scripts
├── docker-compose.yml
├── .env.example
└── README.md
```

## Features

### MVP Features
- Authentication (Register, Login, JWT)
- Candidate profile with onboarding
- Job discovery with location filtering
- Company pages with interview questions
- Resume upload and ATS analysis
- Job/resume matching with skill gap detection
- Company-specific preparation roadmaps
- Application tracker with timeline
- Basic AI Career Copilot

### Future Features
- Coding arena with code execution
- Advanced AI mock interviews
- Recruiter system
- College/TPO system
- Premium subscriptions

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 18+
- Python 3.11+

### Installation

1. Clone the repository
2. Copy `.env.example` to `.env` and configure environment variables
3. Run `docker-compose up -d` to start all services
4. Follow the setup instructions in `docs/setup.md`

### Development

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Documentation

- [Architecture](docs/architecture.md)
- [API Documentation](docs/api.md)
- [Database Schema](docs/database.md)
- [Setup Guide](docs/setup.md)
- [AI Integration](docs/ai.md)
- [Deployment](docs/deployment.md)
- [Product Specs](docs/product.md)

## Environment Variables

See `.env.example` for required environment variables:
- DATABASE_URL
- JWT_SECRET
- REDIS_URL
- GROQ_API_KEY
- LLM_MODEL
- EMBEDDING_MODEL
- Storage configuration

## Security

- JWT authentication with refresh tokens
- Password hashing with bcrypt
- CORS configuration
- Rate limiting
- Input validation
- SQL injection protection via ORM
- Secure file storage for resumes

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## License

Proprietary - All rights reserved

## Support

For support, visit https://devin.ai/support
