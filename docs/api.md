# JobCrack AI - API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication

Most endpoints require JWT authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Response Format

All API responses follow this structure:

### Success Response
```json
{
  "data": { ... },
  "message": "Success message"
}
```

### Error Response
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

## Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (201)**
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "candidate",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200)**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Refresh Token
```http
POST /api/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200)**
```json
{
  "access_token": "new_access_token...",
  "refresh_token": "new_refresh_token...",
  "token_type": "bearer"
}
```

#### Logout
```http
POST /api/auth/logout
Authorization: Bearer <access_token>
```

**Response (200)**
```json
{
  "message": "Successfully logged out"
}
```

### Users

#### Get Current User
```http
GET /api/users/me
Authorization: Bearer <access_token>
```

**Response (200)**
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "candidate",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Get User Profile
```http
GET /api/users/me/profile
Authorization: Bearer <access_token>
```

**Response (200)**
```json
{
  "id": 1,
  "user_id": 1,
  "full_name": "John Doe",
  "phone": "+91 9876543210",
  "current_city": "Bangalore",
  "preferred_locations": ["Bangalore", "Hyderabad"],
  "target_roles": ["Software Engineer", "Full Stack Developer"],
  "experience_years": 2,
  "preferred_work_mode": "hybrid",
  "preferred_salary_min": 800000,
  "preferred_salary_max": 1200000,
  "job_type": "full-time",
  "profile_completeness": 75.0,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-16T14:20:00Z"
}
```

#### Update User Profile
```http
PUT /api/users/me/profile
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "full_name": "John Doe",
  "phone": "+91 9876543210",
  "current_city": "Bangalore",
  "preferred_locations": ["Bangalore", "Hyderabad"],
  "target_roles": ["Software Engineer"],
  "experience_years": 2,
  "preferred_work_mode": "hybrid",
  "preferred_salary_min": 800000,
  "preferred_salary_max": 1200000,
  "job_type": "full-time"
}
```

**Response (200)**
```json
{
  "id": 1,
  "user_id": 1,
  "full_name": "John Doe",
  "phone": "+91 9876543210",
  "current_city": "Bangalore",
  "preferred_locations": ["Bangalore", "Hyderabad"],
  "target_roles": ["Software Engineer"],
  "experience_years": 2,
  "preferred_work_mode": "hybrid",
  "preferred_salary_min": 800000,
  "preferred_salary_max": 1200000,
  "job_type": "full-time",
  "profile_completeness": 85.0,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-16T14:25:00Z"
}
```

#### Add Education
```http
POST /api/users/me/education
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "degree": "B.Tech",
  "branch": "Computer Science",
  "institution": "IIT Bangalore",
  "university": "VTU",
  "graduation_year": 2022,
  "cgpa_percentage": 8.5
}
```

**Response (201)**
```json
{
  "id": 1,
  "profile_id": 1,
  "degree": "B.Tech",
  "branch": "Computer Science",
  "institution": "IIT Bangalore",
  "university": "VTU",
  "graduation_year": 2022,
  "cgpa_percentage": 8.5,
  "created_at": "2024-01-16T10:00:00Z"
}
```

#### Add Skill
```http
POST /api/users/me/skills
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "skill_id": 1,
  "proficiency_level": "intermediate",
  "years_of_experience": 2
}
```

**Response (201)**
```json
{
  "id": 1,
  "profile_id": 1,
  "skill_id": 1,
  "skill_name": "Java",
  "proficiency_level": "intermediate",
  "years_of_experience": 2,
  "created_at": "2024-01-16T10:00:00Z"
}
```

#### Get Profile Completeness
```http
GET /api/users/me/completeness
Authorization: Bearer <access_token>
```

**Response (200)**
```json
{
  "overall": 75.0,
  "personal": 100.0,
  "education": 100.0,
  "skills": 50.0,
  "experience": 0.0,
  "projects": 0.0,
  "certifications": 0.0
}
```

### Jobs

#### List Jobs
```http
GET /api/jobs?search=software&location=bangalore&experience=0-2
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `search` (string): Search query for title, company, skills
- `location` (string): Filter by location
- `job_type` (enum): full-time, part-time, internship, contract
- `work_mode` (enum): remote, hybrid, onsite
- `experience_level` (enum): entry, mid, senior, fresher
- `salary_min` (integer): Minimum salary
- `salary_max` (integer): Maximum salary
- `skills` (array): Filter by skill IDs
- `company_id` (integer): Filter by company
- `sort_by` (string): relevance, newest, match

**Response (200)**
```json
{
  "jobs": [
    {
      "id": 1,
      "title": "Software Engineer",
      "company_name": "TechCorp",
      "company_logo": "https://example.com/logo.png",
      "location": "Bangalore",
      "job_type": "full-time",
      "work_mode": "hybrid",
      "experience_level": "entry",
      "salary_min": 800000,
      "salary_max": 1200000,
      "salary_currency": "INR",
      "posted_date": "2024-01-15T10:00:00Z",
      "match_percentage": 85.0
    }
  ],
  "total": 150,
  "page": 1,
  "per_page": 20
}
```

#### Get Job Details
```http
GET /api/jobs/{job_id}
Authorization: Bearer <access_token>
```

**Response (200)**
```json
{
  "id": 1,
  "company_id": 1,
  "title": "Software Engineer",
  "description": "We are looking for a talented software engineer...",
  "requirements": "Java, Spring Boot, React, SQL",
  "responsibilities": "Develop and maintain applications...",
  "location": "Bangalore",
  "job_type": "full-time",
  "work_mode": "hybrid",
  "experience_level": "entry",
  "experience_years_min": 0,
  "experience_years_max": 2,
  "salary_min": 800000,
  "salary_max": 1200000,
  "salary_currency": "INR",
  "salary_period": "annual",
  "required_skills": [1, 2, 3],
  "preferred_skills": [4, 5],
  "application_url": "https://company.com/apply",
  "application_email": "careers@company.com",
  "apply_deadline": "2024-02-15T23:59:59Z",
  "is_active": true,
  "is_verified": true,
  "posted_date": "2024-01-15T10:00:00Z",
  "expiry_date": "2024-02-15T23:59:59Z",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

### Companies

#### List Companies
```http
GET /api/companies?search=tech&industry=software
Authorization: Bearer <access_token>
```

**Response (200)**
```json
{
  "companies": [
    {
      "id": 1,
      "name": "TechCorp",
      "logo_url": "https://example.com/logo.png",
      "website": "https://techcorp.com",
      "industry": "Software",
      "description": "Leading software company...",
      "locations": ["Bangalore", "Hyderabad"],
      "company_size": "large",
      "founded_year": 2010,
      "is_verified": true,
      "verification_status": "verified",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 50
}
```

#### Get Company Details
```http
GET /api/companies/{company_id}
Authorization: Bearer <access_token>
```

**Response (200)**
```json
{
  "id": 1,
  "name": "TechCorp",
  "logo_url": "https://example.com/logo.png",
  "website": "https://techcorp.com",
  "industry": "Software",
  "description": "Leading software company...",
  "locations": ["Bangalore", "Hyderabad"],
  "company_size": "large",
  "founded_year": 2010,
  "is_verified": true,
  "verification_status": "verified",
  "current_jobs_count": 15,
  "interview_questions_count": 45,
  "coding_questions_count": 30,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
```

### Resumes

#### Upload Resume
```http
POST /api/resumes/upload
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

resume: <file>
```

**Response (201)**
```json
{
  "id": 1,
  "user_id": 1,
  "original_filename": "resume.pdf",
  "file_path": "/uploads/resume_1.pdf",
  "file_size": 245760,
  "file_type": "pdf",
  "is_current": true,
  "version": 1,
  "created_at": "2024-01-16T10:00:00Z"
}
```

#### Analyze Resume
```http
POST /api/resumes/analyze
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "resume_id": 1,
  "job_id": 1
}
```

**Response (200)**
```json
{
  "id": 1,
  "resume_id": 1,
  "job_id": 1,
  "keyword_score": 89.0,
  "structure_score": 92.0,
  "formatting_score": 85.0,
  "overall_score": 88.0,
  "matched_keywords": ["Java", "Spring Boot", "React"],
  "missing_keywords": ["AWS", "Docker", "Kubernetes"],
  "suggested_improvements": [
    "Add AWS certification details",
    "Include more project metrics",
    "Improve formatting consistency"
  ],
  "skill_gaps": [
    {
      "skill": "AWS",
      "importance": "high",
      "suggested_resources": ["AWS Certification Course"]
    }
  ],
  "job_match_score": 78.0,
  "experience_match": {
    "matched": true,
    "details": "Experience aligns with job requirements"
  },
  "education_match": {
    "matched": true,
    "details": "Education meets requirements"
  },
  "created_at": "2024-01-16T10:00:00Z"
}
```

### Matching

#### Get Job Match Analysis
```http
POST /api/matching/jobs/{job_id}/match
Authorization: Bearer <access_token>
```

**Response (200)**
```json
{
  "id": 1,
  "user_id": 1,
  "job_id": 1,
  "overall_score": 82.0,
  "skills_score": 85.0,
  "experience_score": 75.0,
  "education_score": 90.0,
  "location_score": 100.0,
  "matched_skills": ["Java", "Spring Boot", "React", "SQL"],
  "missing_skills": ["AWS", "Docker", "Kubernetes"],
  "relevant_experience": [
    {
      "company": "Previous Company",
      "role": "Software Developer",
      "relevance": "high"
    }
  ],
  "skill_gaps": [
    {
      "skill": "AWS",
      "importance": "high",
      "suggested_learning": "AWS Fundamentals"
    }
  ],
  "suggested_preparation": [
    "Learn AWS basics",
    "Practice Docker and Kubernetes",
    "Study system design patterns"
  ],
  "resume_match_score": 78.0,
  "resume_gaps": [
    "Missing cloud experience",
    "No DevOps projects listed"
  ],
  "created_at": "2024-01-16T10:00:00Z",
  "updated_at": "2024-01-16T10:00:00Z"
}
```

### Preparation

#### Generate Preparation Plan
```http
POST /api/preparation/generate
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "company_id": 1,
  "job_id": 1,
  "role": "Software Engineer",
  "duration_days": 7
}
```

**Response (201)**
```json
{
  "id": 1,
  "user_id": 1,
  "company_id": 1,
  "job_id": 1,
  "plan_name": "TechCorp Software Engineer Preparation",
  "plan_type": "company_specific",
  "duration_days": 7,
  "progress_percentage": 0.0,
  "tasks_completed": 0,
  "total_tasks": 21,
  "is_active": true,
  "start_date": "2024-01-16T10:00:00Z",
  "end_date": "2024-01-23T10:00:00Z",
  "created_at": "2024-01-16T10:00:00Z"
}
```

### Applications

#### List Applications
```http
GET /api/applications
Authorization: Bearer <access_token>
```

**Response (200)**
```json
{
  "applications": [
    {
      "id": 1,
      "user_id": 1,
      "job_id": 1,
      "company_id": 1,
      "resume_id": 1,
      "role": "Software Engineer",
      "company": "TechCorp",
      "location": "Bangalore",
      "status": "interview",
      "job_url": "https://company.com/job/123",
      "application_url": "https://company.com/apply/123",
      "notes": "Technical interview scheduled",
      "interview_date": "2024-01-20T14:00:00Z",
      "next_steps": "Prepare for system design",
      "applied_date": "2024-01-10T10:00:00Z",
      "last_updated": "2024-01-16T10:00:00Z"
    }
  ],
  "total": 12
}
```

#### Create Application
```http
POST /api/applications
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "job_id": 1,
  "company_id": 1,
  "resume_id": 1,
  "role": "Software Engineer",
  "company": "TechCorp",
  "location": "Bangalore",
  "job_url": "https://company.com/job/123",
  "application_url": "https://company.com/apply/123"
}
```

**Response (201)**
```json
{
  "id": 1,
  "user_id": 1,
  "job_id": 1,
  "company_id": 1,
  "resume_id": 1,
  "role": "Software Engineer",
  "company": "TechCorp",
  "location": "Bangalore",
  "status": "applied",
  "job_url": "https://company.com/job/123",
  "application_url": "https://company.com/apply/123",
  "applied_date": "2024-01-16T10:00:00Z",
  "last_updated": "2024-01-16T10:00:00Z"
}
```

### AI

#### AI Chat (Career Copilot)
```http
POST /api/ai/chat
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "message": "Find fresher Java jobs in Hyderabad",
  "context": {
    "job_id": 1,
    "company_id": 1
  }
}
```

**Response (200)**
```json
{
  "response": "I found 15 fresher Java jobs in Hyderabad. Here are the top matches...",
  "sources": [
    {
      "type": "job",
      "id": 1,
      "relevance": 0.95
    }
  ],
  "suggestions": [
    "Consider these companies that are actively hiring",
    "Prepare for Java and Spring Boot interviews"
  ]
}
```

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

## Rate Limiting

- **Default**: 60 requests per minute per user
- **Burst**: Up to 10 requests in 10 seconds
- Headers included: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Pagination

List endpoints support pagination:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20, max: 100)

Response includes:
- `total`: Total number of items
- `page`: Current page
- `per_page`: Items per page
