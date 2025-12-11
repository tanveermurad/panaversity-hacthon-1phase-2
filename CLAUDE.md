# Todo App - Hackathon Phase II

## Project Overview
This is a full-stack todo application built as a monorepo for the hackathon Phase II challenge. It transforms a console app into a modern multi-user web application with persistent storage.

## Technology Stack
- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend**: Python FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth
- **Development**: Claude Code + Spec-Kit Plus

## Spec-Kit Structure
Specifications are organized in `/specs`:
- `/specs/overview.md` - Project overview and status
- `/specs/features/` - Feature specs (what to build)
- `/specs/api/` - API endpoint specifications
- `/specs/database/` - Schema and model specs
- `/specs/ui/` - Component and page specs

## How to Use Specs
1. Always read relevant spec before implementing
2. Reference specs with: `@specs/features/task-crud.md`
3. Update specs if requirements change

## Project Structure
```
hackathon-todo/
├── frontend/          # Next.js application
│   ├── app/          # App Router pages
│   ├── components/   # Reusable UI components
│   ├── lib/          # Utilities and API client
│   └── package.json
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── routes/   # API route handlers
│   │   ├── models/   # SQLModel database models
│   │   └── main.py   # FastAPI entry point
│   └── requirements.txt
├── specs/             # Spec-Kit Plus specifications
└── .spec-kit/         # Spec-Kit configuration
```

## Development Workflow
1. Read spec: `@specs/features/[feature].md`
2. Implement backend: See `@backend/CLAUDE.md`
3. Implement frontend: See `@frontend/CLAUDE.md`
4. Test and iterate

## Commands

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Database Setup
1. Create Neon PostgreSQL database
2. Copy `.env.example` to `.env`
3. Update DATABASE_URL with your Neon connection string
4. Run migrations (if applicable)

### Docker (All Services)
```bash
docker-compose up
```

## Environment Variables

### Backend (.env in backend/)
```
DATABASE_URL=postgresql://user:password@host/database
JWT_SECRET=your-secret-key
ENVIRONMENT=development
```

### Frontend (.env.local in frontend/)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-auth-secret
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=postgresql://user:password@host/database
```

## API Endpoints
All endpoints require authentication (except auth endpoints):
- `GET /api/{user_id}/tasks` - List all tasks
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get task details
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion

## Authentication Flow
1. User signs up/signs in via Better Auth (frontend)
2. Better Auth issues JWT token
3. Frontend includes JWT token in API requests
4. FastAPI backend verifies JWT token
5. API operations scoped to authenticated user

## Key Features (Basic Level)
1. ✅ Create tasks
2. ✅ Read/list tasks
3. ✅ Update tasks
4. ✅ Delete tasks
5. ✅ Mark tasks as complete/incomplete
6. ✅ User authentication (signup/signin)
7. ✅ Multi-user support with data isolation

## Getting Started
1. Clone the repository
2. Set up environment variables
3. Install dependencies (frontend and backend)
4. Start development servers
5. Open http://localhost:3000

## Referencing Specs in Claude Code
```bash
# Implement a feature
@specs/features/task-crud.md implement the create task feature

# Implement API
@specs/api/rest-endpoints.md implement the GET /api/tasks endpoint

# Update database
@specs/database/schema.md add due_date field to tasks

# Full feature across stack
@specs/features/authentication.md implement Better Auth login
```

## Contributing
This is a hackathon project following Spec-Driven Development practices using Claude Code and Spec-Kit Plus.
