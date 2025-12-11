# 🚀 Quick Start Guide

Get the Todo App running in **5 minutes**!

## Prerequisites Checklist

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Git installed
- [ ] Neon account created ([neon.tech](https://neon.tech))

---

## Step 1: Database Setup (2 minutes)

### Create Neon Database

1. Go to [neon.tech](https://neon.tech) and sign up (free)
2. Click **"Create Project"**
3. Choose a region close to you
4. Copy the **connection string** (looks like):
   ```
   postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb
   ```
5. **Important**: Add `?sslmode=require` to the end:
   ```
   postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
   ```

---

## Step 2: Backend Setup (1 minute)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

### Edit `backend/.env`

Replace these values:
```env
DATABASE_URL=<your-neon-connection-string>
JWT_SECRET=<any-random-32-character-string>
```

**Generate JWT secret**:
```bash
# Option 1: Use openssl
openssl rand -hex 32

# Option 2: Use Python
python -c "import secrets; print(secrets.token_hex(32))"

# Option 3: Just make one up (32+ characters)
# Example: my-super-secret-jwt-key-12345678
```

---

## Step 3: Frontend Setup (1 minute)

```bash
# Open new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.local.example .env.local
```

### Edit `frontend/.env.local`

Replace these values:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=<same-jwt-secret-as-backend>
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=<your-neon-connection-string>
```

**Important**: Use the **exact same JWT secret** as backend!

---

## Step 4: Run the App (1 minute)

### Terminal 1: Start Backend

```bash
cd backend
# If not already activated:
source venv/bin/activate  # Windows: venv\Scripts\activate

# Start server
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
Creating database tables...
Database tables created successfully!
```

**Test it**: Open http://localhost:8000/docs

### Terminal 2: Start Frontend

```bash
cd frontend

# Start development server
npm run dev
```

You should see:
```
 ▲ Next.js 15.1.0
 - Local:        http://localhost:3000
```

**Test it**: Open http://localhost:3000

---

## Step 5: Use the App!

### 1. Sign Up
- Go to http://localhost:3000
- Click **"Sign Up"**
- Enter:
  - Email: `test@example.com`
  - Password: `Test1234!` (must have uppercase, lowercase, number, special char)
  - Name: `Test User` (optional)
- Click **"Sign Up"**

### 2. Create Your First Task
- Click **"+ New Task"**
- Title: `Buy groceries`
- Description: `Milk, eggs, bread`
- Click **"Create Task"**

### 3. Manage Tasks
- ✅ Click checkbox to mark complete
- 📝 Click "Edit" to modify
- 🗑️ Click "Delete" (confirm) to remove
- 🔍 Use filter tabs: All / Active / Completed

---

## Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`
```bash
# Solution: Install dependencies
cd backend
pip install -r requirements.txt
```

**Error**: `connection to server ... failed`
```bash
# Solution: Check your DATABASE_URL
# - Make sure it ends with ?sslmode=require
# - Verify credentials are correct
# - Test connection: psql $DATABASE_URL
```

**Error**: `Address already in use`
```bash
# Solution: Kill process on port 8000
# Windows: netstat -ano | findstr :8000
# Linux/Mac: lsof -ti:8000 | xargs kill
```

### Frontend won't start

**Error**: `Cannot find module 'next'`
```bash
# Solution: Install dependencies
cd frontend
npm install
```

**Error**: `Invalid environment variable`
```bash
# Solution: Check .env.local file exists
# - Must be named exactly .env.local (not .env)
# - Check all required variables are set
```

**Error**: `Failed to fetch`
```bash
# Solution: Backend not running
# - Start backend first
# - Check NEXT_PUBLIC_API_URL is correct
```

### Authentication issues

**Error**: `Invalid token`
```bash
# Solution: JWT secrets don't match
# - Backend JWT_SECRET
# - Frontend BETTER_AUTH_SECRET
# - Must be EXACTLY the same string
```

**Can't sign in after signup**
```bash
# Solution: Clear browser storage
# - Open DevTools (F12)
# - Application tab → Storage → Clear site data
# - Try signing up again
```

---

## Verification Checklist

After setup, verify:

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:3000
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] Can access home page
- [ ] Can sign up new user
- [ ] Can sign in
- [ ] Can create task
- [ ] Can edit task
- [ ] Can delete task
- [ ] Can toggle completion
- [ ] Can sign out

---

## Next Steps

### Explore the API
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- Try API endpoints directly

### Read Documentation
- **README.md**: Full setup guide
- **PROJECT_STATUS.md**: Complete feature list
- **CLAUDE.md**: Navigation guide
- **specs/**: Technical specifications

### Customize
- Change color scheme in `frontend/tailwind.config.js`
- Add features following existing patterns
- Deploy to production (see README.md)

---

## Docker Alternative (Optional)

If you prefer Docker:

```bash
# Create .env in root
cp .env.example .env
# Edit with your DATABASE_URL and secrets

# Run everything
docker-compose up --build

# Access: http://localhost:3000
```

---

## Quick Commands Reference

### Backend
```bash
cd backend
source venv/bin/activate          # Activate venv
uvicorn app.main:app --reload     # Start server
pip install -r requirements.txt   # Install deps
```

### Frontend
```bash
cd frontend
npm run dev      # Start dev server
npm run build    # Build for production
npm start        # Run production build
npm run lint     # Check for errors
```

### Docker
```bash
docker-compose up -d         # Start in background
docker-compose logs -f       # View logs
docker-compose down          # Stop all
docker-compose restart       # Restart all
```

---

## Getting Help

1. Check error messages carefully
2. Review this guide's troubleshooting section
3. Check README.md for detailed instructions
4. Review PROJECT_STATUS.md for complete info
5. Check environment variables are correct
6. Verify database connection string

---

## Success! 🎉

You should now have a fully functional Todo application running locally!

**What's working:**
- ✅ User authentication (signup/signin)
- ✅ Create, read, update, delete tasks
- ✅ Mark tasks complete/incomplete
- ✅ Multi-user support with data isolation
- ✅ Persistent storage in Neon PostgreSQL
- ✅ Responsive UI with Tailwind CSS

**Enjoy your new Todo app!**
