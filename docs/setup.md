# JobCrack AI - Setup Guide

## Prerequisites

Before setting up JobCrack AI, ensure you have the following installed:

- **Docker** and **Docker Compose** (for containerized setup)
- **Node.js** 18+ (for local frontend development)
- **Python** 3.11+ (for local backend development)
- **Git** (for version control)

## Quick Start with Docker

The easiest way to get started is using Docker Compose.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd jobcrack-ai
```

### 2. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your configuration
# At minimum, set:
# - DATABASE_URL
# - JWT_SECRET
# - GROQ_API_KEY (if using AI features)
```

### 3. Start All Services

```bash
# Start PostgreSQL, Redis, Backend, and Frontend
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Database**: localhost:5432

### 5. Initialize Database

```bash
# Access the backend container
docker-compose exec backend bash

# Run database migrations
alembic upgrade head

# Exit the container
exit
```

## Local Development Setup

If you prefer to run services locally without Docker:

### Backend Setup

#### 1. Install Python Dependencies

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

#### 2. Configure Environment

```bash
# Copy environment example
cp .env.example .env

# Edit .env with your local configuration
# Set DATABASE_URL to your local PostgreSQL instance
```

#### 3. Start PostgreSQL and Redis

```bash
# Using Docker for databases only
docker-compose up -d postgres redis

# Or use local PostgreSQL and Redis instances
```

#### 4. Run Database Migrations

```bash
alembic upgrade head
```

#### 5. Start the Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at http://localhost:8000

### Frontend Setup

#### 1. Install Node Dependencies

```bash
cd frontend
npm install
```

#### 2. Configure Environment

```bash
# Create local environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

#### 3. Start the Frontend Server

```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## Database Setup

### Using Docker PostgreSQL

```bash
# Start PostgreSQL container
docker-compose up -d postgres

# Wait for database to be ready
docker-compose logs postgres

# Connect to database
docker-compose exec postgres psql -U jobcrack -d jobcrack_db
```

### Using Local PostgreSQL

```bash
# Create database
createdb jobcrack_db

# Create user (if needed)
createuser jobcrack

# Grant permissions
psql -d jobcrack_db -c "GRANT ALL PRIVILEGES ON DATABASE jobcrack_db TO jobcrack;"
```

### Running Migrations

```bash
cd backend

# Generate new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration status
alembic current
```

## Environment Variables

### Required Variables

```bash
# Database
DATABASE_URL=postgresql://jobcrack:password@localhost:5432/jobcrack_db

# Authentication
JWT_SECRET=your-super-secret-jwt-key-change-in-production

# AI/LLM (optional but recommended)
GROQ_API_KEY=your-groq-api-key
```

### Optional Variables

```bash
# Redis
REDIS_URL=redis://localhost:6379/0

# JWT Configuration
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# AI Configuration
LLM_MODEL=llama3-70b-8192
EMBEDDING_MODEL=nomic-embed-text

# Application
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:3000

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# File Upload
MAX_UPLOAD_SIZE=10485760
ALLOWED_FILE_TYPES=.pdf,.docx
UPLOAD_DIR=uploads

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Environment
ENVIRONMENT=development
DEBUG=true
```

## Testing Setup

### Backend Tests

```bash
cd backend

# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

### Frontend Tests

```bash
cd frontend

# Install test dependencies
npm install --save-dev jest @testing-library/react @testing-library/jest-dom

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

## Troubleshooting

### Common Issues

#### Database Connection Failed

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check database logs
docker-compose logs postgres

# Verify connection string in .env
```

#### Port Already in Use

```bash
# Change ports in docker-compose.yml
# Or kill the process using the port

# On Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# On macOS/Linux
lsof -ti:8000 | xargs kill -9
```

#### Module Not Found Errors

```bash
# Backend: Ensure virtual environment is activated
# Frontend: Ensure node_modules are installed
npm install
```

#### Migration Conflicts

```bash
# Resolve migration conflicts
alembic merge -m "merge message" revision1 revision2

# Stamp current database state
alembic stamp head
```

## Development Workflow

### Making Changes

1. **Backend Changes**
   ```bash
   # Edit code in backend/app/
   # Restart backend server (or use --reload)
   uvicorn app.main:app --reload
   ```

2. **Frontend Changes**
   ```bash
   # Edit code in frontend/app/ or frontend/components/
   # Frontend auto-reloads with npm run dev
   ```

3. **Database Changes**
   ```bash
   # Modify models in backend/app/models/
   # Generate migration
   alembic revision --autogenerate -m "description"
   # Apply migration
   alembic upgrade head
   ```

### Code Quality

```bash
# Backend linting
cd backend
flake8 app/
black app/
mypy app/

# Frontend linting
cd frontend
npm run lint
```

## Production Deployment

### Building for Production

#### Backend

```bash
cd backend

# Build Docker image
docker build -t jobcrack-backend .

# Or use production requirements
pip install -r requirements.txt --no-cache-dir
```

#### Frontend

```bash
cd frontend

# Build production bundle
npm run build

# Start production server
npm start
```

### Environment Configuration

```bash
# Use production environment variables
ENVIRONMENT=production
DEBUG=false

# Use strong JWT secret
JWT_SECRET=<generate-strong-secret>

# Use production database
DATABASE_URL=<production-database-url>

# Configure CORS for production domain
CORS_ORIGINS=https://yourdomain.com
```

### Security Considerations

- Change all default passwords
- Use strong JWT secrets
- Enable HTTPS in production
- Configure proper CORS origins
- Set up SSL certificates
- Enable rate limiting
- Configure firewall rules
- Regular security updates

## Monitoring and Logging

### Backend Logs

```bash
# View backend logs
docker-compose logs -f backend

# Or with local setup
uvicorn app.main:app --log-level info
```

### Database Monitoring

```bash
# Connect to database
docker-compose exec postgres psql -U jobcrack -d jobcrack_db

# Check database size
SELECT pg_size_pretty(pg_database_size('jobcrack_db'));

# Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## Additional Resources

- [Architecture Documentation](architecture.md)
- [API Documentation](api.md)
- [Database Documentation](database.md)
- [AI Integration Guide](ai.md)
- [Deployment Guide](deployment.md)

## Support

For issues and questions:
- Check existing GitHub issues
- Review documentation
- Contact development team
