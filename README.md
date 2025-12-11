# Todo App - Hackathon Phase II

A full-stack todo application built with **Next.js 16+**, **FastAPI**, **SQLModel**, and **Neon PostgreSQL** following Spec-Driven Development practices using **Claude Code** and **Spec-Kit Plus**.

## Features

- ✅ User authentication (signup/signin) with Better Auth
- ✅ Create, read, update, and delete tasks
- ✅ Mark tasks as complete/incomplete
- ✅ Multi-user support with data isolation
- ✅ Persistent storage in Neon PostgreSQL
- ✅ JWT token-based API security
- ✅ Responsive UI with Tailwind CSS
- ✅ RESTful API design

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 16+ (App Router), TypeScript, Tailwind CSS |
| **Backend** | Python FastAPI |
| **ORM** | SQLModel |
| **Database** | Neon Serverless PostgreSQL |
| **Authentication** | Better Auth (JWT tokens) |
| **Development** | Claude Code + Spec-Kit Plus |

## Project Structure

```
hackathon-todo/
├── frontend/              # Next.js application
│   ├── app/              # App Router pages
│   │   ├── (auth)/       # Authentication pages
│   │   ├── (dashboard)/  # Protected dashboard pages
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/       # Reusable UI components
│   ├── lib/              # Utilities and API client
│   ├── package.json
│   └── .env.local.example
│
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── models/       # SQLModel database models
│   │   ├── routes/       # API route handlers
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── middleware/   # Auth middleware
│   │   ├── config.py     # Configuration
│   │   ├── db.py         # Database connection
│   │   └── main.py       # FastAPI entry point
│   ├── requirements.txt
│   └── .env.example
│
├── specs/                # Spec-Kit Plus specifications
│   ├── features/         # Feature specifications
│   ├── api/              # API endpoint specs
│   ├── database/         # Database schema specs
│   └── ui/               # UI component specs
│
├── .spec-kit/            # Spec-Kit configuration
├── CLAUDE.md             # Root navigation guide
└── README.md             # This file
```

## Getting Started

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.10+
- **Neon PostgreSQL** account ([neon.tech](https://neon.tech))
- **Git**

### 1. Clone the Repository

```bash
git clone <repository-url>
cd hackathon-todo
```

### 2. Set Up Neon Database

1. Create a free account at [neon.tech](https://neon.tech)
2. Create a new project and database
3. Copy the connection string (format: `postgresql://user:password@host/database`)

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Edit .env and add your configuration:
# - DATABASE_URL (your Neon connection string)
# - JWT_SECRET (generate a secure random string, min 32 chars)
```

**Example .env file:**
```env
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
JWT_SECRET=your-super-secret-key-min-32-characters-long-please
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000
API_HOST=0.0.0.0
API_PORT=8000
```

**Start the backend server:**
```bash
# Run with auto-reload
uvicorn app.main:app --reload

# Server will start at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

### 4. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Create .env.local file from example
cp .env.local.example .env.local

# Edit .env.local and add your configuration:
# - NEXT_PUBLIC_API_URL (backend URL)
# - BETTER_AUTH_SECRET (same as backend JWT_SECRET)
# - DATABASE_URL (same Neon connection string)
```

**Example .env.local file:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-super-secret-key-min-32-characters-long-please
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
```

**Start the frontend server:**
```bash
# Run development server
npm run dev

# Application will start at http://localhost:3000
```

### 5. Access the Application

1. Open your browser to `http://localhost:3000`
2. Click "Sign Up" to create an account
3. Enter your email, password, and name
4. After signup, you'll be automatically logged in
5. Start creating and managing your tasks!

## API Documentation

### Interactive API Docs

Once the backend is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Register new user |
| POST | `/api/auth/signin` | Login user |
| GET | `/api/auth/me` | Get current user |

#### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all user tasks |
| POST | `/api/{user_id}/tasks` | Create new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

All task endpoints require authentication via JWT token in the `Authorization: Bearer <token>` header.

## Database Schema

### Users Table
- `id` (UUID): Primary key
- `email` (VARCHAR): Unique user email
- `password_hash` (VARCHAR): Bcrypt hashed password
- `name` (VARCHAR): User display name
- `created_at` (TIMESTAMP): Account creation time

### Tasks Table
- `id` (INTEGER): Primary key (auto-increment)
- `user_id` (UUID): Foreign key to users
- `title` (VARCHAR): Task title
- `description` (TEXT): Task description (optional)
- `completed` (BOOLEAN): Completion status
- `created_at` (TIMESTAMP): Creation time
- `updated_at` (TIMESTAMP): Last update time

## Development Workflow

This project follows **Spec-Driven Development** using Claude Code and Spec-Kit Plus:

1. **Read Specifications**: All features are documented in `/specs`
2. **Implement Backend**: Follow guidelines in `backend/CLAUDE.md`
3. **Implement Frontend**: Follow guidelines in `frontend/CLAUDE.md`
4. **Test**: Verify functionality works end-to-end
5. **Iterate**: Update specs if requirements change

### Using Specs

```bash
# View feature spec
cat specs/features/task-crud.md

# View API spec
cat specs/api/rest-endpoints.md

# View database schema
cat specs/database/schema.md
```

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Deployment

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Manual Deployment

#### Backend (FastAPI)

1. Set environment variables on your hosting platform
2. Install dependencies: `pip install -r requirements.txt`
3. Run with Gunicorn: `gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker`

#### Frontend (Next.js)

1. Set environment variables
2. Build: `npm run build`
3. Start: `npm start`

Or deploy to **Vercel** (recommended for Next.js):
```bash
npm install -g vercel
vercel
```

## Troubleshooting

### Backend Issues

**Database Connection Error:**
- Ensure Neon connection string includes `?sslmode=require`
- Check network connectivity to Neon
- Verify credentials are correct

**JWT Token Error:**
- Ensure `JWT_SECRET` is at least 32 characters
- Ensure frontend and backend use the same secret
- Check token is being sent in Authorization header

### Frontend Issues

**API Connection Error:**
- Ensure backend is running on http://localhost:8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify CORS is configured correctly in backend

**Authentication Error:**
- Check Better Auth configuration
- Ensure `BETTER_AUTH_SECRET` matches `JWT_SECRET`
- Verify database connection for Better Auth

## Contributing

This is a hackathon project. To contribute:

1. Read the specifications in `/specs`
2. Follow the coding patterns in `CLAUDE.md` files
3. Maintain consistency with existing code
4. Update specs if adding new features

## License

This project is created for the Hackathon Phase II challenge.

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Neon PostgreSQL](https://neon.tech/)
- [Better Auth Documentation](https://www.better-auth.com/)
- [Claude Code](https://claude.com/claude-code)
- [Spec-Kit Plus](https://github.com/specify)

## Support

For questions or issues:
1. Check the `/specs` documentation
2. Review `CLAUDE.md` files for guidance
3. Consult the API documentation at `/docs`

---

**Built with Claude Code and Spec-Kit Plus** 🚀
