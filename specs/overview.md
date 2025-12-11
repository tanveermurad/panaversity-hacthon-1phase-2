# Todo App - Project Overview

## Hackathon Phase II Challenge

Transform a console todo app into a modern multi-user web application with persistent storage using Claude Code and Spec-Kit Plus.

## Objective
Implement all 5 Basic Level features as a web application with:
- RESTful API endpoints
- Responsive frontend interface
- Persistent storage in Neon Serverless PostgreSQL
- User authentication (signup/signin) using Better Auth

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16+ (App Router) |
| Backend | Python FastAPI |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Spec-Driven | Claude Code + Spec-Kit Plus |
| Authentication | Better Auth |

## Core Features (Basic Level)

### 1. Task CRUD Operations
- ✅ Create new tasks
- ✅ Read/list all user tasks
- ✅ Update existing tasks
- ✅ Delete tasks
- ✅ Mark tasks as complete/incomplete

### 2. Multi-User Support
- ✅ User registration (signup)
- ✅ User authentication (signin)
- ✅ User-specific task isolation
- ✅ Secure API endpoints

### 3. Data Persistence
- ✅ PostgreSQL database (Neon)
- ✅ Relational data model
- ✅ Data integrity and constraints

## Architecture

### Frontend (Next.js 16+)
```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── signin/
│   │   └── signup/
│   ├── (dashboard)/
│   │   ├── tasks/
│   │   └── layout.tsx
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── task-list.tsx
│   ├── task-item.tsx
│   ├── task-form.tsx
│   └── auth-form.tsx
└── lib/
    ├── api.ts
    ├── auth.ts
    └── types.ts
```

### Backend (FastAPI)
```
backend/
├── app/
│   ├── routes/
│   │   ├── tasks.py
│   │   └── auth.py
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   ├── middleware/
│   │   └── auth.py
│   ├── db.py
│   ├── config.py
│   └── main.py
└── requirements.txt
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | User registration |
| POST | `/api/auth/signin` | User authentication |
| GET | `/api/{user_id}/tasks` | List all tasks |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

## Database Schema

### Users Table
- `id`: string (primary key, UUID)
- `email`: string (unique, not null)
- `password_hash`: string (not null)
- `name`: string
- `created_at`: timestamp

### Tasks Table
- `id`: integer (primary key, auto-increment)
- `user_id`: string (foreign key → users.id)
- `title`: string (not null)
- `description`: text (nullable)
- `completed`: boolean (default: false)
- `created_at`: timestamp
- `updated_at`: timestamp

## Authentication Flow

1. **User Registration**
   - User submits email/password via frontend
   - Better Auth handles registration
   - User record created in database

2. **User Login**
   - User submits credentials
   - Better Auth verifies and issues JWT token
   - Token stored in frontend (secure cookie/localStorage)

3. **Authenticated API Requests**
   - Frontend includes JWT token in Authorization header
   - FastAPI middleware verifies token
   - Extract user_id from token
   - Scope API operations to authenticated user

## Security Considerations

1. **JWT Token Verification**
   - FastAPI verifies JWT signature
   - Check token expiration
   - Extract user claims

2. **Data Isolation**
   - All task operations scoped to user_id
   - Prevent unauthorized access to other users' data

3. **Input Validation**
   - Pydantic models for request validation
   - SQL injection prevention (SQLModel/SQLAlchemy)
   - XSS prevention (React escaping)

## Development Phases

### Phase 1: Backend Setup ✅
- [x] Set up FastAPI project structure
- [x] Configure Neon PostgreSQL connection
- [x] Create SQLModel models
- [x] Implement database migrations

### Phase 2: API Implementation ✅
- [x] Create task CRUD endpoints
- [x] Implement authentication endpoints
- [x] Add JWT verification middleware
- [x] Test all API endpoints

### Phase 3: Frontend Setup ✅
- [x] Set up Next.js 16+ with App Router
- [x] Configure Tailwind CSS
- [x] Set up Better Auth
- [x] Create API client library

### Phase 4: UI Implementation ✅
- [x] Build authentication pages (signin/signup)
- [x] Create task list component
- [x] Create task form component
- [x] Implement task CRUD operations in UI

### Phase 5: Integration & Testing ✅
- [x] Connect frontend to backend API
- [x] Test authentication flow
- [x] Test all task operations
- [x] Verify data persistence

### Phase 6: Deployment 🚀
- [ ] Configure environment variables
- [ ] Set up Docker containers
- [ ] Deploy to production
- [ ] Final testing

## Success Criteria

- ✅ User can register and sign in
- ✅ User can create, read, update, and delete tasks
- ✅ User can mark tasks as complete/incomplete
- ✅ Tasks persist across sessions
- ✅ Users can only access their own tasks
- ✅ Responsive UI works on mobile and desktop
- ✅ API follows RESTful conventions
- ✅ Code follows Spec-Driven Development practices

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Neon PostgreSQL](https://neon.tech/)
- [Better Auth Documentation](https://www.better-auth.com/)
- [Spec-Kit Plus](https://github.com/specify)

## Notes

- This project uses a monorepo structure for easier development
- Claude Code and Spec-Kit Plus guide the development process
- All specifications are maintained in the `/specs` directory
- Follow the guidelines in `CLAUDE.md` for navigation and patterns
