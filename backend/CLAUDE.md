# Backend Guidelines

## Stack
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT tokens (verified from Better Auth)
- **Python Version**: 3.10+

## Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app entry point
│   ├── config.py         # Configuration and environment variables
│   ├── db.py             # Database connection and session management
│   ├── models/           # SQLModel database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── routes/           # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── middleware/       # Custom middleware
│   │   ├── __init__.py
│   │   └── auth.py
│   └── schemas/          # Pydantic request/response schemas
│       ├── __init__.py
│       ├── user.py
│       └── task.py
├── requirements.txt
├── .env.example
└── README.md
```

## API Conventions

### Routing
- All routes under `/api/`
- Version routes if needed: `/api/v1/`, `/api/v2/`
- Follow RESTful conventions
- Group related endpoints in router files

### Request/Response
- Use Pydantic models for validation
- Return JSON responses
- Include appropriate HTTP status codes
- Follow consistent response format

### Error Handling
- Use HTTPException for errors
- Include descriptive error messages
- Use proper status codes (400, 401, 403, 404, 500)
- Log errors for debugging

### Example Route
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.db import get_session
from app.middleware.auth import verify_token
from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter(prefix="/api/{user_id}/tasks", tags=["tasks"])

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    authenticated_user_id: str = Depends(verify_token)
):
    # Verify user_id matches authenticated user
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )

    # Create task
    task = Task(user_id=user_id, **task_data.dict())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

## Database

### Connection
- Use SQLModel for ORM operations
- Connection string from environment variable
- Neon requires SSL: `?sslmode=require`
- Use connection pooling (NullPool for serverless)

### Models
- Define models in `app/models/`
- Use SQLModel (combines SQLAlchemy and Pydantic)
- Include table name, columns, constraints
- Add relationships where needed

### Migrations
- Use Alembic for database migrations
- Or use SQLModel.metadata.create_all() for simple cases
- Always test migrations before production

### Session Management
```python
from sqlmodel import Session
from app.db import engine

def get_session():
    """Dependency for database session"""
    with Session(engine) as session:
        yield session
```

## Authentication

### JWT Verification
- Verify JWT tokens from Better Auth
- Extract user_id from token payload
- Implement middleware for protected routes
- Handle token expiration and invalid tokens

### Middleware Example
```python
from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from app.config import settings

security = HTTPBearer()

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> str:
    """Verify JWT token and return user_id"""
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
```

## Configuration

### Environment Variables
Store sensitive data in `.env` file (never commit to git):

```env
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
JWT_SECRET=your-secret-key-min-32-chars
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000
```

### Config Module
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: str = "http://localhost:3000"

    class Config:
        env_file = ".env"

settings = Settings()
```

## Error Handling

### Standard Errors
```python
from fastapi import HTTPException, status

# 400 Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid input"
)

# 401 Unauthorized
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid or expired token"
)

# 403 Forbidden
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Forbidden"
)

# 404 Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Task not found"
)

# 500 Internal Server Error
# Let FastAPI handle these automatically
```

### Global Exception Handler
```python
from fastapi import Request, status
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the error
    print(f"Error: {exc}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )
```

## CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing

### Test Structure
```
tests/
├── __init__.py
├── conftest.py          # Pytest fixtures
├── test_auth.py         # Authentication tests
├── test_tasks.py        # Task CRUD tests
└── test_database.py     # Database tests
```

### Example Test
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_task():
    # Setup: create user and get token
    response = client.post(
        "/api/auth/signup",
        json={
            "email": "test@example.com",
            "password": "Test123!",
        }
    )
    token = response.json()["token"]
    user_id = response.json()["user"]["id"]

    # Test: create task
    response = client.post(
        f"/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test task",
            "description": "Test description"
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Test task"
```

## Running the Server

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the Python module
python -m uvicorn app.main:app --reload
```

### Production
```bash
# Use Gunicorn with Uvicorn workers
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Use in routes
logger.info(f"User {user_id} created task {task.id}")
logger.error(f"Error creating task: {e}")
```

## Best Practices

### Code Organization
- Keep routes focused and small
- Extract business logic to service functions
- Use dependency injection (Depends)
- Follow single responsibility principle

### Database
- Always use parameterized queries (automatic with SQLModel)
- Close sessions properly (use context managers)
- Handle database errors gracefully
- Use transactions for multi-step operations

### Security
- Never log sensitive data (passwords, tokens)
- Validate all user input
- Use HTTPS in production
- Implement rate limiting
- Keep dependencies updated

### Performance
- Use database indexes
- Implement caching where appropriate
- Use async/await for I/O operations
- Monitor query performance
- Optimize N+1 queries

### Documentation
- Add docstrings to functions
- Use type hints
- Document complex logic
- Keep API docs updated (FastAPI auto-generates)

## Deployment

### Environment Variables
Set these in your deployment platform:
- DATABASE_URL
- JWT_SECRET
- ENVIRONMENT=production
- CORS_ORIGINS (your frontend URL)

### Health Check
Implement a health check endpoint:
```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }
```

### Docker
Use the provided Dockerfile and docker-compose.yml

## Troubleshooting

### Common Issues

**Connection Error to Neon:**
- Ensure DATABASE_URL includes `?sslmode=require`
- Check network connectivity
- Verify credentials

**JWT Verification Fails:**
- Ensure JWT_SECRET matches Better Auth secret
- Check token expiration
- Verify token format (Bearer <token>)

**CORS Errors:**
- Check CORS_ORIGINS includes frontend URL
- Verify credentials and headers are allowed

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Neon Documentation](https://neon.tech/docs/)
- API Spec: `@specs/api/rest-endpoints.md`
- Database Schema: `@specs/database/schema.md`
