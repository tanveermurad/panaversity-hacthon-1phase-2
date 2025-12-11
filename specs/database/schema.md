# Database Schema Specification

## Overview
Database schema for the Todo application using PostgreSQL (Neon) with SQLModel ORM.

## Database Provider
- **Provider**: Neon Serverless PostgreSQL
- **Connection**: Pooled connections via connection string
- **SSL**: Required (Neon enforces SSL)

## Tables

### 1. Users Table

Stores user account information.

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**
- `id` (UUID): Primary key, auto-generated UUID
- `email` (VARCHAR 255): User's email address, must be unique
- `password_hash` (VARCHAR 255): Bcrypt hashed password
- `name` (VARCHAR 255): User's display name (optional)
- `created_at` (TIMESTAMP): Account creation timestamp

**Constraints:**
- PRIMARY KEY on `id`
- UNIQUE constraint on `email`
- NOT NULL on `email`, `password_hash`

**Indexes:**
```sql
CREATE INDEX idx_users_email ON users(email);
```

### 2. Tasks Table

Stores todo tasks with user ownership.

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Columns:**
- `id` (SERIAL): Primary key, auto-incrementing integer
- `user_id` (UUID): Foreign key to users table
- `title` (VARCHAR 200): Task title (required)
- `description` (TEXT): Task description (optional)
- `completed` (BOOLEAN): Completion status, defaults to false
- `created_at` (TIMESTAMP): Creation timestamp
- `updated_at` (TIMESTAMP): Last update timestamp

**Constraints:**
- PRIMARY KEY on `id`
- FOREIGN KEY on `user_id` references `users(id)`
- ON DELETE CASCADE: Delete tasks when user is deleted
- NOT NULL on `user_id`, `title`

**Indexes:**
```sql
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
```

## Relationships

```
users (1) ──< (many) tasks
  id ────────────── user_id
```

- **One-to-Many**: One user can have many tasks
- **Cascade Delete**: When a user is deleted, all their tasks are deleted

## SQLModel Models

### User Model

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### Task Model

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## Pydantic Schemas (Request/Response)

### User Schemas

```python
from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    name: Optional[str]
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str
```

### Task Schemas

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
```

## Database Connection

### Connection Configuration

```python
from sqlmodel import create_engine, Session
from sqlalchemy.pool import NullPool
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Neon requires SSL
if DATABASE_URL and "sslmode" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries (disable in production)
    poolclass=NullPool,  # For serverless
)

def get_session():
    """Dependency for getting database session"""
    with Session(engine) as session:
        yield session
```

## Migrations

### Initial Migration (Create Tables)

```python
from sqlmodel import SQLModel
from app.db import engine
from app.models import User, Task

def create_tables():
    """Create all tables in the database"""
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()
    print("Tables created successfully")
```

### Running Migrations

```bash
# Create tables
python -m app.db

# Or use Alembic for more advanced migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Data Integrity Rules

### User Table
1. Email must be valid format
2. Email must be unique across all users
3. Password must be hashed (never store plain text)
4. User ID is auto-generated UUID

### Task Table
1. Title is required (1-200 characters)
2. Description is optional (max 1000 characters recommended)
3. Task must belong to a valid user (foreign key)
4. Completed defaults to false
5. Timestamps auto-generated and auto-updated

### Referential Integrity
1. All tasks must reference a valid user
2. Deleting a user cascades to delete all their tasks
3. User cannot be deleted if they have active references (prevented by CASCADE)

## Query Patterns

### Common Queries

#### Get all tasks for a user
```python
from sqlmodel import select

def get_user_tasks(session: Session, user_id: uuid.UUID):
    statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    tasks = session.exec(statement).all()
    return tasks
```

#### Get incomplete tasks
```python
def get_incomplete_tasks(session: Session, user_id: uuid.UUID):
    statement = select(Task).where(
        Task.user_id == user_id,
        Task.completed == False
    )
    tasks = session.exec(statement).all()
    return tasks
```

#### Update task
```python
def update_task(session: Session, task_id: int, user_id: uuid.UUID, **kwargs):
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()
    if task:
        for key, value in kwargs.items():
            setattr(task, key, value)
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
    return task
```

#### Delete task
```python
def delete_task(session: Session, task_id: int, user_id: uuid.UUID):
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id
    )
    task = session.exec(statement).first()
    if task:
        session.delete(task)
        session.commit()
        return True
    return False
```

## Performance Optimization

### Indexes
- `idx_users_email`: Fast user lookup by email (login)
- `idx_tasks_user_id`: Fast filtering of tasks by user
- `idx_tasks_completed`: Fast filtering by completion status
- `idx_tasks_created_at`: Fast sorting by creation date

### Connection Pooling
- Use NullPool for serverless (Neon)
- Connection pooling handled by Neon
- Close connections properly after use

### Query Optimization
- Always filter by user_id to use index
- Limit results for large datasets
- Use select only needed columns
- Avoid N+1 queries (use joins if needed)

## Security Considerations

### SQL Injection Prevention
- Use SQLModel parameterized queries (automatic)
- Never concatenate user input into SQL
- Validate all input with Pydantic models

### Data Access Control
- Always filter queries by authenticated user_id
- Never allow cross-user data access
- Verify user_id matches authenticated user

### Password Storage
- Hash passwords with bcrypt (salt rounds >= 10)
- Never store or log plain-text passwords
- Use secure random salts

### Connection Security
- Always use SSL/TLS for database connections
- Store connection strings in environment variables
- Never commit credentials to version control

## Backup and Recovery

### Neon Automatic Backups
- Neon provides automatic backups
- Point-in-time recovery available
- Consult Neon documentation for retention policy

### Manual Backup
```bash
# Backup database
pg_dump $DATABASE_URL > backup.sql

# Restore database
psql $DATABASE_URL < backup.sql
```

## Monitoring

### Metrics to Monitor
- Connection pool usage
- Query performance (slow queries)
- Database size growth
- Index usage statistics
- Error rates

### Logging
- Log all database errors
- Log slow queries (> 1 second)
- Monitor connection failures
- Track failed transactions

## Environment Variables

```env
# Database connection
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# Connection pooling (if needed)
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_TIMEOUT=30
```

## Testing Database

### Test Database Setup
```python
from sqlmodel import create_engine, Session, SQLModel
from app.models import User, Task

# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL)

def setup_test_db():
    SQLModel.metadata.create_all(test_engine)

def teardown_test_db():
    SQLModel.metadata.drop_all(test_engine)
```

## Future Schema Enhancements (Out of Scope)

### Potential Additions
- `categories` table for task categorization
- `tags` table with many-to-many relationship
- `task_history` table for audit trail
- `user_preferences` table for settings
- `due_date` column in tasks table
- `priority` column in tasks table
- `shared_tasks` table for collaboration

### Migration Strategy
- Use Alembic for schema versioning
- Test migrations on staging before production
- Always create backup before migration
- Write reversible migrations (up and down)
