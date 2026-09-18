# JobCrack AI - Database Documentation

## Database Overview

JobCrack AI uses PostgreSQL as the primary database with pgvector extension for vector search capabilities.

## Database Schema

### Core Tables

#### users
Stores user authentication and basic information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | User ID |
| email | VARCHAR(255) | UNIQUE, NOT NULL, INDEXED | User email |
| hashed_password | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| role | ENUM | NOT NULL, DEFAULT 'candidate' | User role (candidate/recruiter/admin) |
| is_active | BOOLEAN | DEFAULT TRUE | Account active status |
| is_verified | BOOLEAN | DEFAULT FALSE | Email verification status |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation time |
| updated_at | TIMESTAMP | ON UPDATE NOW() | Last update time |

**Relationships:**
- One-to-one with `profiles`
- One-to-many with `resumes`, `applications`, `interview_sessions`, `notifications`

#### profiles
Stores detailed user profile information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Profile ID |
| user_id | INTEGER | FOREIGN KEY(users), UNIQUE, NOT NULL | User ID |
| full_name | VARCHAR(255) | | Full name |
| phone | VARCHAR(20) | | Phone number |
| current_city | VARCHAR(100) | | Current location |
| preferred_locations | JSON | | List of preferred cities |
| target_roles | JSON | | List of target job roles |
| experience_years | INTEGER | DEFAULT 0 | Years of experience |
| preferred_work_mode | VARCHAR(20) | | remote/hybrid/onsite |
| preferred_salary_min | INTEGER | | Minimum expected salary |
| preferred_salary_max | INTEGER | | Maximum expected salary |
| job_type | VARCHAR(20) | | full-time/part-time/internship |
| profile_completeness | FLOAT | DEFAULT 0.0 | Profile completeness percentage |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | ON UPDATE NOW() | Last update time |

**Relationships:**
- Many-to-one with `users`
- One-to-many with `education`, `user_skills`, `experiences`, `projects`, `certifications`

#### education
Stores user education history.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Education ID |
| profile_id | INTEGER | FOREIGN KEY(profiles), NOT NULL | Profile ID |
| degree | VARCHAR(100) | | Degree (B.Tech, M.Tech, etc.) |
| branch | VARCHAR(100) | | Branch/Field of study |
| institution | VARCHAR(255) | | Institution name |
| university | VARCHAR(255) | | University name |
| graduation_year | INTEGER | | Year of graduation |
| cgpa_percentage | FLOAT | | CGPA or percentage |
| start_date | TIMESTAMP | | Start date |
| end_date | TIMESTAMP | | End date |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | ON UPDATE NOW() | Last update time |

#### skills
Master table for available skills.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Skill ID |
| name | VARCHAR(100) | UNIQUE, NOT NULL, INDEXED | Skill name |
| category | VARCHAR(50) | | Skill category |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |

**Relationships:**
- One-to-many with `user_skills`, `job_skills`

#### user_skills
Junction table for user skills with proficiency.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | User skill ID |
| profile_id | INTEGER | FOREIGN KEY(profiles), NOT NULL | Profile ID |
| skill_id | INTEGER | FOREIGN KEY(skills), NOT NULL | Skill ID |
| proficiency_level | VARCHAR(20) | | beginner/intermediate/advanced/expert |
| years_of_experience | INTEGER | DEFAULT 0 | Years of experience |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | ON UPDATE NOW() | Last update time |

#### experiences
Stores user work experience.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Experience ID |
| profile_id | INTEGER | FOREIGN KEY(profiles), NOT NULL | Profile ID |
| company | VARCHAR(255) | | Company name |
| role | VARCHAR(255) | | Job role |
| location | VARCHAR(100) | | Work location |
| employment_type | VARCHAR(20) | | full-time/part-time/contract/internship |
| work_mode | VARCHAR(20) | | remote/hybrid/onsite |
| description | TEXT | | Job description |
| start_date | TIMESTAMP | | Start date |
| end_date | TIMESTAMP | | End date |
| is_current | BOOLEAN | DEFAULT FALSE | Currently working here |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | ON UPDATE NOW() | Last update time |

#### projects
Stores user projects.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Project ID |
| profile_id | INTEGER | FOREIGN KEY(profiles), NOT NULL | Profile ID |
| title | VARCHAR(255) | | Project title |
| description | TEXT | | Project description |
| technologies | VARCHAR(500) | | Comma-separated technologies |
| project_url | VARCHAR(500) | | Project URL |
| github_url | VARCHAR(500) | | GitHub URL |
| start_date | TIMESTAMP | | Start date |
| end_date | TIMESTAMP | | End date |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | ON UPDATE NOW() | Last update time |

#### certifications
Stores user certifications.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Certification ID |
| profile_id | INTEGER | FOREIGN KEY(profiles), NOT NULL | Profile ID |
| name | VARCHAR(255) | | Certification name |
| issuer | VARCHAR(255) | | Issuing organization |
| issue_date | TIMESTAMP | | Issue date |
| expiry_date | TIMESTAMP | | Expiry date |
| credential_id | VARCHAR(100) | | Credential ID |
| credential_url | VARCHAR(500) | | Credential URL |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | ON UPDATE NOW() | Last update time |

#### companies
Stores company information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Company ID |
| name | VARCHAR(255) | UNIQUE, NOT NULL, INDEXED | Company name |
| logo_url | VARCHAR(500) | | Logo URL |
| website | VARCHAR(500) | | Company website |
| industry | VARCHAR(100) | | Industry |
| description | TEXT | | Company description |
| locations | JSON | | List of office locations |
| company_size | VARCHAR(20) | | startup/small/medium/large/enterprise |
| founded_year | INTEGER | | Year founded |
| is_verified | BOOLEAN | DEFAULT FALSE | Verification status |
| verification_status | VARCHAR(20) | | pending/verified/rejected |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | ON UPDATE NOW() | Last update time |

**Relationships:**
- One-to-many with `jobs`, `interview_questions`, `coding_questions`

#### jobs
Stores job postings.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Job ID |
| company_id | INTEGER | FOREIGN KEY(companies), NOT NULL | Company ID |
| title | VARCHAR(255) | NOT NULL, INDEXED | Job title |
| description | TEXT | | Job description |
| requirements | TEXT | | Job requirements |
| responsibilities | TEXT | | Job responsibilities |
| location | VARCHAR(100) | INDEXED | Job location |
| job_type | ENUM | DEFAULT 'full-time' | full-time/part-time/internship/contract |
| work_mode | ENUM | DEFAULT 'onsite' | remote/hybrid/onsite |
| experience_level | ENUM | DEFAULT 'entry' | entry/mid/senior/lead/fresher |
| experience_years_min | INTEGER | | Minimum experience |
| experience_years_max | INTEGER | | Maximum experience |
| salary_min | INTEGER | | Minimum salary |
| salary_max | INTEGER | | Maximum salary |
| salary_currency | VARCHAR(3) | DEFAULT 'INR' | Currency code |
| salary_period | VARCHAR(20) | | annual/monthly/hourly |
| required_skills | JSON | | List of required skill IDs |
| preferred_skills | JSON | | List of preferred skill IDs |
| application_url | VARCHAR(500) | | Application URL |
| application_email | VARCHAR(255) | | Application email |
| apply_deadline | TIMESTAMP | | Application deadline |
| source | VARCHAR(50) | | Job source |
| source_url | VARCHAR(500) | | Source URL |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| is_verified | BOOLEAN | DEFAULT FALSE | Verification status |
| verification_status | VARCHAR(20) | | pending/verified/rejected |
| posted_date | TIMESTAMP | DEFAULT NOW() | Posting date |
| expiry_date | TIMESTAMP | | Expiry date |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | ON UPDATE NOW() | Last update time |

**Relationships:**
- Many-to-one with `companies`
- One-to-many with `job_skills`, `job_matches`, `applications`

#### job_skills
Junction table for job skills.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Job skill ID |
| job_id | INTEGER | FOREIGN KEY(jobs), NOT NULL | Job ID |
| skill_id | INTEGER | FOREIGN KEY(skills), NOT NULL | Skill ID |
| is_required | BOOLEAN | DEFAULT TRUE | Required vs preferred |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |

#### resumes
Stores user resume files and parsed data.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Resume ID |
| user_id | INTEGER | FOREIGN KEY(users), NOT NULL | User ID |
| original_filename | VARCHAR(255) | | Original filename |
| file_path | VARCHAR(500) | | Stored file path |
| file_size | INTEGER | | File size in bytes |
| file_type | VARCHAR(10) | | pdf/docx |
| parsed_data | JSON | | Parsed resume content |
| is_current | BOOLEAN | DEFAULT TRUE | Current resume flag |
| version | INTEGER | DEFAULT 1 | Version number |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | ON UPDATE NOW() | Last update time |

**Relationships:**
- Many-to-one with `users`
- One-to-many with `resume_versions`, `resume_analyses`

#### resume_versions
Stores different versions of resumes.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Version ID |
| resume_id | INTEGER | FOREIGN KEY(resumes), NOT NULL | Resume ID |
| job_id | INTEGER | FOREIGN KEY(jobs) | Target job ID |
| version_name | VARCHAR(255) | | Version name |
| content | TEXT | | Full resume content |
| changes | JSON | | List of changes |
| is_ai_tailored | BOOLEAN | DEFAULT FALSE | AI-tailored flag |
| tailoring_job_id | INTEGER | FOREIGN KEY(jobs) | Tailoring job ID |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |

#### resume_analyses
Stores ATS analysis results.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Analysis ID |
| resume_id | INTEGER | FOREIGN KEY(resumes), NOT NULL | Resume ID |
| job_id | INTEGER | FOREIGN KEY(jobs) | Target job ID |
| keyword_score | FLOAT | | Keyword match score |
| structure_score | FLOAT | | Structure score |
| formatting_score | FLOAT | | Formatting score |
| overall_score | FLOAT | | Overall score |
| matched_keywords | JSON | | Matched keywords |
| missing_keywords | JSON | | Missing keywords |
| suggested_improvements | JSON | | Improvement suggestions |
| skill_gaps | JSON | | Skill gaps |
| job_match_score | FLOAT | | Job match score |
| experience_match | JSON | | Experience match details |
| education_match | JSON | | Education match details |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |

#### job_matches
Stores job matching analysis results.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Match ID |
| user_id | INTEGER | FOREIGN KEY(users), NOT NULL | User ID |
| job_id | INTEGER | FOREIGN KEY(jobs), NOT NULL | Job ID |
| overall_score | FLOAT | | Overall match score |
| skills_score | FLOAT | | Skills match score |
| experience_score | FLOAT | | Experience match score |
| education_score | FLOAT | | Education match score |
| location_score | FLOAT | | Location match score |
| matched_skills | JSON | | Matched skills |
| missing_skills | JSON | | Missing skills |
| relevant_experience | JSON | | Relevant experience |
| skill_gaps | JSON | | Skill gaps |
| suggested_preparation | JSON | | Preparation suggestions |
| resume_match_score | FLOAT | | Resume match score |
| resume_gaps | JSON | | Resume gaps |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | ON UPDATE NOW() | Last update time |

#### interview_questions
Stores interview questions by company.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Question ID |
| company_id | INTEGER | FOREIGN KEY(companies) | Company ID |
| question | TEXT | NOT NULL | Question text |
| answer | TEXT | | Answer text |
| explanation | TEXT | | Explanation |
| round | ENUM | | aptitude/coding/technical/hr/behavioral |
| topic | VARCHAR(100) | | Question topic |
| difficulty | ENUM | DEFAULT 'medium' | easy/medium/hard |
| role | VARCHAR(100) | | Target role |
| source | VARCHAR(100) | | Question source |
| verification_status | ENUM | DEFAULT 'community_reported' | official/verified/community_reported |
| verified_by | INTEGER | FOREIGN KEY(users) | Verified by user |
| times_asked | INTEGER | DEFAULT 0 | Times asked count |
| last_asked | TIMESTAMP | | Last asked date |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | ON UPDATE NOW() | Last update time |

#### interview_sessions
Stores AI mock interview sessions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Session ID |
| user_id | INTEGER | FOREIGN KEY(users), NOT NULL | User ID |
| job_id | INTEGER | FOREIGN KEY(jobs) | Target job ID |
| company_id | INTEGER | FOREIGN KEY(companies) | Target company ID |
| interview_type | VARCHAR(50) | | technical/hr/behavioral/coding/full |
| role | VARCHAR(100) | | Target role |
| difficulty | ENUM | DEFAULT 'medium' | easy/medium/hard |
| status | VARCHAR(20) | | in_progress/completed/abandoned |
| score | INTEGER | | Session score |
| feedback | JSON | | AI feedback |
| technical_feedback | TEXT | | Technical feedback |
| communication_feedback | TEXT | | Communication feedback |
| problem_solving_feedback | TEXT | | Problem-solving feedback |
| started_at | TIMESTAMP | DEFAULT NOW() | Start time |
| completed_at | TIMESTAMP | | Completion time |

**Relationships:**
- Many-to-one with `users`
- One-to-many with `interview_answers`

#### interview_answers
Stores answers within interview sessions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Answer ID |
| session_id | INTEGER | FOREIGN KEY(interview_sessions), NOT NULL | Session ID |
| question_id | INTEGER | FOREIGN KEY(interview_questions) | Question ID |
| question | TEXT | | Question text |
| answer | TEXT | | User answer |
| ai_feedback | TEXT | | AI feedback |
| score | INTEGER | | Answer score |
| asked_at | TIMESTAMP | DEFAULT NOW() | Question asked time |
| answered_at | TIMESTAMP | | Answer time |

#### applications
Stores job applications.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Application ID |
| user_id | INTEGER | FOREIGN KEY(users), NOT NULL | User ID |
| job_id | INTEGER | FOREIGN KEY(jobs) | Target job ID |
| company_id | INTEGER | FOREIGN KEY(companies) | Company ID |
| resume_id | INTEGER | FOREIGN KEY(resumes) | Used resume ID |
| role | VARCHAR(255) | | Applied role |
| company | VARCHAR(255) | | Company name |
| location | VARCHAR(100) | | Job location |
| status | ENUM | DEFAULT 'applied' | applied/assessment/interview/hr_interview/offer/rejected/withdrawn |
| job_url | VARCHAR(500) | | Job URL |
| application_url | VARCHAR(500) | | Application URL |
| notes | TEXT | | Notes |
| interview_date | TIMESTAMP | | Interview date |
| next_steps | TEXT | | Next steps |
| applied_date | TIMESTAMP | DEFAULT NOW() | Application date |
| last_updated | TIMESTAMP | ON UPDATE NOW() | Last update time |

**Relationships:**
- Many-to-one with `users`, `jobs`, `companies`, `resumes`
- One-to-many with `application_events`

#### application_events
Stores application timeline events.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Event ID |
| application_id | INTEGER | FOREIGN KEY(applications), NOT NULL | Application ID |
| event_type | VARCHAR(50) | | applied/assessment/interview/offer/rejected/note |
| status | VARCHAR(50) | | Event status |
| description | TEXT | | Event description |
| notes | TEXT | | Event notes |
| interview_date | TIMESTAMP | | Interview date |
| event_date | TIMESTAMP | DEFAULT NOW() | Event date |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |

#### preparation_plans
Stores preparation plans.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Plan ID |
| user_id | INTEGER | FOREIGN KEY(users), NOT NULL | User ID |
| company_id | INTEGER | FOREIGN KEY(companies) | Target company ID |
| job_id | INTEGER | FOREIGN KEY(jobs) | Target job ID |
| plan_name | VARCHAR(255) | | Plan name |
| plan_type | VARCHAR(50) | | company_specific/role_specific/general |
| duration_days | INTEGER | | Plan duration in days |
| progress_percentage | FLOAT | DEFAULT 0.0 | Progress percentage |
| tasks_completed | INTEGER | DEFAULT 0 | Completed tasks count |
| total_tasks | INTEGER | DEFAULT 0 | Total tasks count |
| tasks | JSON | | Structured tasks |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| start_date | TIMESTAMP | DEFAULT NOW() | Start date |
| end_date | TIMESTAMP | | End date |
| completed_at | TIMESTAMP | | Completion date |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | ON UPDATE NOW() | Last update time |

#### preparation_tasks
Stores individual preparation tasks.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Task ID |
| plan_id | INTEGER | FOREIGN KEY(preparation_plans), NOT NULL | Plan ID |
| title | VARCHAR(255) | | Task title |
| description | TEXT | | Task description |
| task_type | VARCHAR(50) | | study/practice/coding/interview/quiz |
| topic | VARCHAR(100) | | Task topic |
| difficulty | VARCHAR(20) | | Task difficulty |
| content | JSON | | Task content |
| resources | JSON | | Task resources |
| status | ENUM | DEFAULT 'pending' | pending/in_progress/completed/skipped |
| progress | FLOAT | DEFAULT 0.0 | Task progress |
| day_number | INTEGER | | Day number in plan |
| estimated_hours | INTEGER | | Estimated hours |
| due_date | TIMESTAMP | | Due date |
| completed_at | TIMESTAMP | | Completion date |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | ON UPDATE NOW() | Last update time |

#### learning_topics
Master table for learning topics.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Topic ID |
| title | VARCHAR(255) | NOT NULL | Topic title |
| description | TEXT | | Topic description |
| category | VARCHAR(50) | | Topic category |
| difficulty | VARCHAR(20) | | Topic difficulty |
| content | TEXT | | Topic content |
| resources | JSON | | Learning resources |
| prerequisites | JSON | | Prerequisite topic IDs |
| estimated_hours | INTEGER | | Estimated learning hours |
| popularity | INTEGER | DEFAULT 0 | Popularity score |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | ON UPDATE NOW() | Last update time |

#### notifications
Stores user notifications.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Notification ID |
| user_id | INTEGER | FOREIGN KEY(users), NOT NULL | User ID |
| type | ENUM | NOT NULL | job_match/application_update/interview_reminder/preparation_reminder/resume_improvement/system |
| title | VARCHAR(255) | NOT NULL | Notification title |
| message | TEXT | NOT NULL | Notification message |
| action_url | VARCHAR(500) | | Action URL |
| action_text | VARCHAR(100) | | Action button text |
| metadata | JSON | | Additional metadata |
| is_read | BOOLEAN | DEFAULT FALSE | Read status |
| read_at | TIMESTAMP | | Read timestamp |
| email_sent | BOOLEAN | DEFAULT FALSE | Email sent status |
| push_sent | BOOLEAN | DEFAULT FALSE | Push sent status |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |

**Relationships:**
- Many-to-one with `users`

#### notification_preferences
Stores user notification preferences.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Preference ID |
| user_id | INTEGER | FOREIGN KEY(users), UNIQUE, NOT NULL | User ID |
| email_job_matches | BOOLEAN | DEFAULT TRUE | Email job matches |
| email_application_updates | BOOLEAN | DEFAULT TRUE | Email application updates |
| email_interview_reminders | BOOLEAN | DEFAULT TRUE | Email interview reminders |
| email_preparation_reminders | BOOLEAN | DEFAULT TRUE | Email preparation reminders |
| push_job_matches | BOOLEAN | DEFAULT TRUE | Push job matches |
| push_application_updates | BOOLEAN | DEFAULT TRUE | Push application updates |
| push_interview_reminders | BOOLEAN | DEFAULT TRUE | Push interview reminders |
| push_preparation_reminders | BOOLEAN | DEFAULT TRUE | Push preparation reminders |
| email_frequency | VARCHAR(20) | DEFAULT 'daily' | Email frequency |
| push_frequency | VARCHAR(20) | DEFAULT 'instant' | Push frequency |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | ON UPDATE NOW() | Last update time |

#### reports
Stores content reports.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Report ID |
| reporter_id | INTEGER | FOREIGN KEY(users) | Reporter user ID |
| report_type | VARCHAR(50) | | job/company/question/content/user |
| entity_type | VARCHAR(50) | | Entity type |
| entity_id | INTEGER | | Entity ID |
| reason | VARCHAR(255) | | Report reason |
| description | TEXT | | Report description |
| status | ENUM | DEFAULT 'pending' | pending/reviewed/resolved/dismissed |
| reviewed_by | INTEGER | FOREIGN KEY(users) | Reviewer user ID |
| review_notes | TEXT | | Review notes |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | ON UPDATE NOW() | Last update time |

#### admin_actions
Stores admin action logs.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO INCREMENT | Action ID |
| admin_id | INTEGER | FOREIGN KEY(users) | Admin user ID |
| action_type | VARCHAR(50) | | create/update/delete/verify/reject |
| entity_type | VARCHAR(50) | | job/company/question/user |
| entity_id | INTEGER | | Entity ID |
| changes | JSON | | Description of changes |
| reason | TEXT | | Action reason |
| ip_address | VARCHAR(45) | | IP address |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |

## Database Migrations

### Running Migrations

```bash
# Generate new migration
cd backend
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history

# View current version
alembic current
```

### Initial Setup

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Generate initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply initial migration
alembic upgrade head
```

## Database Performance

### Indexes

The following columns are indexed for performance:
- `users.email`
- `jobs.title`
- `jobs.location`
- `skills.name`
- `companies.name`

### Connection Pooling

```python
# Database connection pool configuration
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

### Query Optimization

- Use eager loading for relationships to avoid N+1 queries
- Apply appropriate indexes on frequently queried columns
- Use pagination for list endpoints
- Implement caching for frequently accessed data

## Backup and Recovery

### Backup

```bash
# Full database backup
pg_dump -U jobcrack -d jobcrack_db > backup.sql

# Schema-only backup
pg_dump -U jobcrack -d jobcrack_db --schema-only > schema.sql

# Data-only backup
pg_dump -U jobcrack -d jobcrack_db --data-only > data.sql
```

### Restore

```bash
# Restore from backup
psql -U jobcrack -d jobcrack_db < backup.sql
```

## Data Retention

- User data: Retained indefinitely unless account deletion
- Job data: Retained for 1 year after expiry
- Application data: Retained indefinitely
- Notification data: Retained for 90 days
- Analytics data: Aggregated and retained for 1 year
