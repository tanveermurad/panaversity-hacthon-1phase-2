# API Specification: REST Endpoints

## Base URL
```
Development: http://localhost:8000
Production: https://your-domain.com
```

## Authentication
All endpoints (except auth endpoints) require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Response Format

### Success Response
```json
{
  "data": {...},
  "message": "Success message"
}
```

### Error Response
```json
{
  "detail": "Error message",
  "code": "ERROR_CODE"
}
```

## HTTP Status Codes
- `200 OK`: Successful GET/PUT/PATCH request
- `201 Created`: Successful POST request
- `204 No Content`: Successful DELETE request
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict (e.g., duplicate email)
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

---

## Authentication Endpoints

### 1. Sign Up

Create a new user account.

**Endpoint:** `POST /api/auth/signup`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

**Validation:**
- `email`: Required, valid email format, unique
- `password`: Required, min 8 chars, must contain uppercase, lowercase, number, special char
- `name`: Optional, max 255 chars

**Success Response (201 Created):**
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses:**
- `400`: Invalid email format or password requirements not met
- `409`: Email already exists

---

### 2. Sign In

Authenticate user and receive JWT token.

**Endpoint:** `POST /api/auth/signin`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Success Response (200 OK):**
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses:**
- `401`: Invalid credentials

---

### 3. Get Current User

Get authenticated user information.

**Endpoint:** `GET /api/auth/me`

**Headers:**
```
Authorization: Bearer <token>
```

**Success Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `401`: Invalid or expired token

---

## Task Endpoints

All task endpoints require authentication and verify that the `user_id` in the URL matches the authenticated user.

### 4. List All Tasks

Get all tasks for the authenticated user.

**Endpoint:** `GET /api/{user_id}/tasks`

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters (Optional):**
- `completed`: Filter by completion status (true/false)
- `limit`: Number of results (default: 100, max: 1000)
- `offset`: Pagination offset (default: 0)

**Success Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": 2,
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Finish report",
      "description": null,
      "completed": true,
      "created_at": "2024-01-14T09:00:00Z",
      "updated_at": "2024-01-15T14:00:00Z"
    }
  ],
  "total": 2
}
```

**Error Responses:**
- `401`: Invalid token
- `403`: user_id doesn't match authenticated user

---

### 5. Create Task

Create a new task for the authenticated user.

**Endpoint:** `POST /api/{user_id}/tasks`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Validation:**
- `title`: Required, 1-200 characters
- `description`: Optional, max 1000 characters

**Success Response (201 Created):**
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `400`: Invalid input (title missing or too long)
- `401`: Invalid token
- `403`: user_id doesn't match authenticated user

---

### 6. Get Task Details

Get details of a specific task.

**Endpoint:** `GET /api/{user_id}/tasks/{task_id}`

**Headers:**
```
Authorization: Bearer <token>
```

**Success Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Error Responses:**
- `401`: Invalid token
- `403`: user_id doesn't match authenticated user
- `404`: Task not found or doesn't belong to user

---

### 7. Update Task

Update an existing task.

**Endpoint:** `PUT /api/{user_id}/tasks/{task_id}`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "Buy groceries and supplies",
  "description": "Milk, eggs, bread, cleaning supplies",
  "completed": false
}
```

**Validation:**
- `title`: Optional, 1-200 characters
- `description`: Optional, max 1000 characters
- `completed`: Optional, boolean

**Success Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and supplies",
  "description": "Milk, eggs, bread, cleaning supplies",
  "completed": false,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T15:45:00Z"
}
```

**Error Responses:**
- `400`: Invalid input
- `401`: Invalid token
- `403`: user_id doesn't match authenticated user
- `404`: Task not found

---

### 8. Delete Task

Delete a task permanently.

**Endpoint:** `DELETE /api/{user_id}/tasks/{task_id}`

**Headers:**
```
Authorization: Bearer <token>
```

**Success Response (204 No Content):**
```
(Empty response body)
```

**Error Responses:**
- `401`: Invalid token
- `403`: user_id doesn't match authenticated user
- `404`: Task not found

---

### 9. Toggle Task Completion

Toggle the completion status of a task.

**Endpoint:** `PATCH /api/{user_id}/tasks/{task_id}/complete`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body (Optional):**
```json
{
  "completed": true
}
```

If no body provided, the completion status will be toggled (true ↔ false).

**Success Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T16:00:00Z"
}
```

**Error Responses:**
- `401`: Invalid token
- `403`: user_id doesn't match authenticated user
- `404`: Task not found

---

## Rate Limiting

To prevent abuse, the following rate limits apply:

- **Authentication endpoints**: 5 requests per minute per IP
- **Task endpoints**: 100 requests per minute per user

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642254000
```

**Rate Limit Exceeded (429 Too Many Requests):**
```json
{
  "detail": "Rate limit exceeded. Try again in 60 seconds.",
  "code": "RATE_LIMIT_EXCEEDED"
}
```

---

## CORS Configuration

The API allows requests from the following origins:
```
Development: http://localhost:3000
Production: https://your-frontend-domain.com
```

**Allowed Methods:** GET, POST, PUT, PATCH, DELETE, OPTIONS

**Allowed Headers:** Content-Type, Authorization

---

## Request/Response Examples

### cURL Examples

#### Sign Up
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "name": "John Doe"
  }'
```

#### Create Task
```bash
curl -X POST http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }'
```

#### List Tasks
```bash
curl -X GET http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440000/tasks \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

#### Update Task
```bash
curl -X PUT http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440000/tasks/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "title": "Buy groceries and supplies",
    "completed": true
  }'
```

#### Delete Task
```bash
curl -X DELETE http://localhost:8000/api/550e8400-e29b-41d4-a716-446655440000/tasks/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Error Codes Reference

| Code | Description |
|------|-------------|
| INVALID_CREDENTIALS | Email or password is incorrect |
| EMAIL_EXISTS | Email already registered |
| INVALID_TOKEN | JWT token is invalid or expired |
| FORBIDDEN | User not authorized for this resource |
| NOT_FOUND | Requested resource not found |
| VALIDATION_ERROR | Input validation failed |
| RATE_LIMIT_EXCEEDED | Too many requests |
| SERVER_ERROR | Internal server error |

---

## Versioning

The API is currently at version 1. Future versions will be accessible via:
```
/api/v2/...
```

The current endpoints will remain at `/api/...` for backward compatibility.

---

## Health Check

**Endpoint:** `GET /health`

**Success Response (200 OK):**
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

**Use Case:** Load balancers and monitoring tools can use this endpoint to check API health.

---

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

These are auto-generated from FastAPI and provide a live testing interface.
