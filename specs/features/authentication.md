# Feature Spec: User Authentication

## Overview
Implement user authentication using Better Auth with signup and signin functionality, JWT token management, and secure API access.

## User Stories

### US-1: User Registration
**As a** new user
**I want to** create an account
**So that** I can access the todo application

**Acceptance Criteria:**
- User can enter email and password
- User can optionally enter their name
- Email must be unique in the system
- Password must meet security requirements
- User receives confirmation after successful registration
- User is automatically logged in after registration
- JWT token is issued upon registration

### US-2: User Login
**As a** registered user
**I want to** sign in to my account
**So that** I can access my tasks

**Acceptance Criteria:**
- User can enter email and password
- Credentials are verified against database
- JWT token is issued upon successful login
- User is redirected to dashboard
- Error message shown for invalid credentials
- Token is stored securely in browser

### US-3: User Logout
**As a** logged-in user
**I want to** sign out
**So that** my account is secure

**Acceptance Criteria:**
- User can click logout button
- JWT token is cleared from browser
- User is redirected to signin page
- User cannot access protected pages after logout

### US-4: Protected Routes
**As a** system
**I want to** protect authenticated pages
**So that** only logged-in users can access them

**Acceptance Criteria:**
- Unauthenticated users redirected to signin
- JWT token is verified on each request
- Expired tokens are handled gracefully
- User session persists across page refreshes

## Authentication Architecture

### Better Auth (Frontend)
Better Auth runs in the Next.js application and handles:
- User signup/signin forms
- Session management
- JWT token generation
- Secure token storage
- Token refresh

### FastAPI (Backend)
FastAPI verifies JWT tokens and:
- Validates token signature
- Checks token expiration
- Extracts user_id from token
- Protects API endpoints
- Returns 401 for invalid tokens

### JWT Token Flow
1. User submits credentials to Better Auth (Next.js)
2. Better Auth verifies credentials against database
3. Better Auth generates JWT token with user info
4. Token stored in secure HTTP-only cookie or localStorage
5. Frontend includes token in Authorization header
6. FastAPI middleware verifies token
7. FastAPI allows/denies request based on verification

## Technical Specifications

### User Data Model
```typescript
interface User {
  id: string;           // UUID
  email: string;        // Unique
  password_hash: string; // Bcrypt hashed
  name?: string;
  created_at: Date;
}
```

### JWT Token Structure
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

## API Endpoints

### Sign Up
```
POST /api/auth/signup
Body: {
  email: string;
  password: string;
  name?: string;
}
Response: {
  user: User;
  token: string;
}
```

### Sign In
```
POST /api/auth/signin
Body: {
  email: string;
  password: string;
}
Response: {
  user: User;
  token: string;
}
```

### Get Current User
```
GET /api/auth/me
Headers: { Authorization: Bearer <token> }
Response: User
```

### Sign Out
```
POST /api/auth/signout
Headers: { Authorization: Bearer <token> }
Response: { success: true }
```

## Frontend Implementation

### Better Auth Configuration
```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: {
    url: process.env.DATABASE_URL!,
  },
  secret: process.env.BETTER_AUTH_SECRET!,
  jwt: {
    expiresIn: "7d",
    algorithm: "HS256",
  },
  session: {
    cookieCache: {
      enabled: true,
      maxAge: 60 * 60 * 24 * 7, // 7 days
    },
  },
});
```

### Auth Pages
- `/signin` - Sign in form
- `/signup` - Sign up form
- Both should redirect to dashboard if already authenticated

### Protected Layout
- Check authentication status
- Redirect to signin if not authenticated
- Show loading state during check

## Backend Implementation

### JWT Verification Middleware
```python
# app/middleware/auth.py
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

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
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Protected Routes
```python
@router.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    authenticated_user_id: str = Depends(verify_token)
):
    # Verify user_id matches authenticated user
    if user_id != authenticated_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # Return user's tasks
    ...
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

## Security Considerations

### Password Security
- Never store plain-text passwords
- Use bcrypt with salt rounds >= 10
- Implement rate limiting on auth endpoints
- Lock accounts after multiple failed attempts

### JWT Security
- Use strong secret key (min 256 bits)
- Set appropriate expiration times
- Implement token refresh mechanism
- Store tokens securely (HTTP-only cookies preferred)
- Don't include sensitive data in JWT payload

### HTTPS
- Always use HTTPS in production
- Secure cookie flags (HttpOnly, Secure, SameSite)

### CORS
- Configure CORS properly
- Allow only trusted origins
- Include credentials if using cookies

## Error Handling

### Common Errors
- 400: Invalid input (email format, password requirements)
- 401: Invalid credentials or token
- 403: Forbidden (user_id mismatch)
- 409: Email already exists (signup)
- 500: Server error

### Error Messages
- Be generic for security (don't reveal if email exists)
- Provide helpful validation messages
- Log errors server-side for debugging

## Testing Requirements

### Backend Tests
- Test signup with valid/invalid data
- Test signin with valid/invalid credentials
- Test JWT token generation/verification
- Test token expiration handling
- Test user_id verification in protected routes
- Test rate limiting

### Frontend Tests
- Test signup form validation
- Test signin form validation
- Test successful authentication flow
- Test redirect logic for protected routes
- Test token storage and retrieval
- Test logout functionality

## Integration with Better Auth

### Setup Steps
1. Install Better Auth: `npm install better-auth`
2. Configure Better Auth with database connection
3. Set up environment variables
4. Create auth API routes in Next.js
5. Implement auth client for frontend
6. Configure FastAPI JWT verification

### Environment Variables

**Frontend (.env.local):**
```
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=postgresql://...
```

**Backend (.env):**
```
JWT_SECRET=same-secret-as-better-auth
DATABASE_URL=postgresql://...
```

## User Experience

### Sign Up Flow
1. User navigates to `/signup`
2. User fills in email, password, name
3. Form validates input client-side
4. Submit sends request to Better Auth
5. Success: redirect to dashboard with welcome message
6. Error: show specific validation errors

### Sign In Flow
1. User navigates to `/signin`
2. User enters email and password
3. Submit sends request to Better Auth
4. Success: redirect to dashboard
5. Error: show "Invalid credentials" message
6. Remember user on device (optional checkbox)

### Protected Page Access
1. User tries to access protected page
2. Check for valid JWT token
3. Valid: render page
4. Invalid/Missing: redirect to `/signin`
5. After signin: redirect back to intended page

## Performance Considerations
- Cache user data after authentication
- Implement token refresh without re-authentication
- Optimize database queries for user lookup
- Use connection pooling for database

## Monitoring and Logging
- Log all authentication attempts
- Monitor failed login attempts
- Track token refresh patterns
- Alert on suspicious activity

## Compliance
- GDPR: Allow users to delete accounts
- Store minimal user data
- Provide privacy policy
- Allow password reset (future enhancement)

## Dependencies
- Better Auth library
- JWT library (PyJWT for Python)
- Bcrypt library for password hashing
- Database connection (Neon PostgreSQL)

## Future Enhancements (Out of Scope)
- Password reset via email
- Email verification
- OAuth providers (Google, GitHub)
- Two-factor authentication
- Account deletion
- Profile management
- Remember me functionality
