# Feature Spec: Task CRUD Operations

## Overview
Implement full CRUD (Create, Read, Update, Delete) operations for todo tasks with user isolation.

## User Stories

### US-1: Create Task
**As a** logged-in user
**I want to** create a new task
**So that** I can track things I need to do

**Acceptance Criteria:**
- User can enter a task title (required)
- User can optionally enter a task description
- New task defaults to incomplete status
- Task is saved to database with user_id
- User sees confirmation/updated task list

### US-2: View All Tasks
**As a** logged-in user
**I want to** see all my tasks
**So that** I can review what I need to do

**Acceptance Criteria:**
- User sees a list of all their tasks
- Tasks show title, description, and completion status
- Tasks are ordered by creation date (newest first)
- Empty state shown when no tasks exist
- User only sees their own tasks (not other users')

### US-3: View Task Details
**As a** logged-in user
**I want to** view details of a specific task
**So that** I can see all information about it

**Acceptance Criteria:**
- User can click on a task to view details
- Details include: title, description, status, creation date
- User can only view their own tasks

### US-4: Update Task
**As a** logged-in user
**I want to** edit an existing task
**So that** I can update information or fix mistakes

**Acceptance Criteria:**
- User can edit task title
- User can edit task description
- Changes are saved to database
- Updated timestamp is recorded
- User can only edit their own tasks

### US-5: Delete Task
**As a** logged-in user
**I want to** delete a task
**So that** I can remove tasks I no longer need

**Acceptance Criteria:**
- User can delete any of their tasks
- Confirmation prompt before deletion
- Task is permanently removed from database
- User sees updated task list
- User can only delete their own tasks

### US-6: Toggle Task Completion
**As a** logged-in user
**I want to** mark tasks as complete or incomplete
**So that** I can track my progress

**Acceptance Criteria:**
- User can toggle task completion status
- Completed tasks are visually distinct
- Status change persists to database
- User can only toggle their own tasks

## Functional Requirements

### FR-1: Task Data Model
```typescript
interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: Date;
  updated_at: Date;
}
```

### FR-2: Validation Rules
- Title: Required, 1-200 characters
- Description: Optional, max 1000 characters
- User must be authenticated
- User can only access their own tasks

### FR-3: Error Handling
- 400: Invalid input data
- 401: User not authenticated
- 403: User trying to access another user's task
- 404: Task not found
- 500: Server error

## API Requirements

### Create Task
```
POST /api/{user_id}/tasks
Body: { title, description? }
Response: Task object
```

### List Tasks
```
GET /api/{user_id}/tasks
Response: Task[]
```

### Get Task
```
GET /api/{user_id}/tasks/{id}
Response: Task object
```

### Update Task
```
PUT /api/{user_id}/tasks/{id}
Body: { title?, description?, completed? }
Response: Task object
```

### Delete Task
```
DELETE /api/{user_id}/tasks/{id}
Response: { success: true }
```

### Toggle Completion
```
PATCH /api/{user_id}/tasks/{id}/complete
Response: Task object
```

## UI Requirements

### Task List View
- Display all user tasks
- Show task title and completion status
- Click task to view/edit details
- Button to create new task
- Toggle completion with checkbox
- Delete button for each task

### Task Form
- Input for title (required)
- Textarea for description (optional)
- Submit button
- Cancel button
- Form validation with error messages

### Task Item Component
- Display task title
- Display task description (if exists)
- Checkbox for completion status
- Edit button
- Delete button
- Creation/update timestamp

## Technical Considerations

### Backend (FastAPI)
- Use SQLModel for database operations
- Implement middleware for user authentication
- Validate user_id matches authenticated user
- Use Pydantic models for request/response validation
- Implement proper error handling

### Frontend (Next.js)
- Use server components for initial data fetching
- Use client components for interactive elements
- Implement optimistic UI updates
- Handle loading and error states
- Use React Hook Form for form handling

### Database
- Index on user_id for efficient filtering
- Index on completed for status filtering
- Foreign key constraint to users table
- ON DELETE CASCADE for user deletion

## Testing Requirements

### Backend Tests
- Test CRUD operations
- Test user isolation (can't access other users' tasks)
- Test input validation
- Test authentication middleware
- Test error handling

### Frontend Tests
- Test task list rendering
- Test task creation form
- Test task update functionality
- Test task deletion with confirmation
- Test completion toggle

## Security Considerations
- All endpoints require authentication
- Verify user_id matches authenticated user
- Prevent SQL injection (use parameterized queries)
- Sanitize user input
- Rate limiting on API endpoints

## Performance Considerations
- Database queries should use indexes
- Pagination for large task lists (future enhancement)
- Optimistic UI updates for better UX
- Cache user data where appropriate

## Non-Functional Requirements
- API response time < 200ms for CRUD operations
- UI should be responsive on mobile devices
- Support for 1000+ tasks per user
- Data persistence and durability

## Dependencies
- User authentication must be implemented first
- Database schema must be created
- API client library must be available

## Future Enhancements (Out of Scope)
- Task categories/tags
- Due dates and reminders
- Task priorities
- Search and filtering
- Sorting options
- Task sharing between users
