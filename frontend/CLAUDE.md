# Frontend Guidelines

## Stack
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Authentication**: JWT tokens (from FastAPI backend)

## Project Structure
```
frontend/
├── app/
│   ├── (auth)/              # Authentication routes
│   │   ├── signin/
│   │   └── signup/
│   ├── (dashboard)/         # Protected routes
│   │   └── tasks/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Home page
│   └── globals.css          # Global styles
├── components/              # Reusable components
│   ├── TaskItem.tsx
│   ├── TaskForm.tsx
│   └── TaskList.tsx
├── lib/                     # Utilities
│   ├── api.ts              # API client
│   ├── types.ts            # TypeScript types
│   └── utils.ts            # Helper functions
├── public/                  # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── next.config.js
```

## App Router Conventions

### Route Groups
- `(auth)` - Authentication pages (signin, signup)
- `(dashboard)` - Protected pages requiring authentication

### File Conventions
- `page.tsx` - Route page component
- `layout.tsx` - Shared layout
- `loading.tsx` - Loading UI
- `error.tsx` - Error UI
- `not-found.tsx` - 404 page

## API Client Usage

### Import and Use
```typescript
import { api, getErrorMessage } from "@/lib/api";

// Sign up
try {
  const response = await api.signup({
    email: "user@example.com",
    password: "SecurePass123!",
    name: "John Doe"
  });
  console.log(response.user, response.token);
} catch (err) {
  console.error(getErrorMessage(err));
}

// Get tasks
const { tasks, total } = await api.getTasks(userId);

// Create task
const newTask = await api.createTask(userId, {
  title: "Buy groceries",
  description: "Milk, eggs, bread"
});

// Update task
const updatedTask = await api.updateTask(userId, taskId, {
  title: "Updated title",
  completed: true
});

// Delete task
await api.deleteTask(userId, taskId);

// Toggle completion
const task = await api.toggleTaskCompletion(userId, taskId);
```

### Authentication
```typescript
// Check if authenticated
if (api.isAuthenticated()) {
  // User is signed in
}

// Get stored user
import { getStoredUser } from "@/lib/utils";
const user = getStoredUser();

// Sign out
api.signout();
router.push("/");
```

## Component Patterns

### Client Components
Use `"use client"` directive for interactive components:

```typescript
"use client";

import { useState } from "react";

export default function MyComponent() {
  const [state, setState] = useState("");
  // Component logic
}
```

### Server Components (Default)
No directive needed. Use for static content and data fetching:

```typescript
export default function Page() {
  return <div>Static content</div>;
}
```

## State Management

### Local State
Use React hooks for component-level state:

```typescript
const [tasks, setTasks] = useState<Task[]>([]);
const [loading, setLoading] = useState(false);
const [error, setError] = useState("");
```

### URL State
Use Next.js router for URL-based state:

```typescript
import { useRouter, useSearchParams } from "next/navigation";

const router = useRouter();
const searchParams = useSearchParams();

// Navigate
router.push("/tasks");

// Get query params
const filter = searchParams.get("filter");
```

## Form Handling

### Controlled Forms
```typescript
const [formData, setFormData] = useState({ title: "", description: "" });

const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();
  await api.createTask(userId, formData);
};

return (
  <form onSubmit={handleSubmit}>
    <input
      value={formData.title}
      onChange={(e) => setFormData({ ...formData, title: e.target.value })}
    />
  </form>
);
```

## Styling with Tailwind

### Utility Classes
```tsx
<div className="flex items-center justify-between p-4 bg-white rounded-lg shadow-md">
  <h1 className="text-2xl font-bold text-gray-900">Title</h1>
  <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
    Click
  </button>
</div>
```

### Custom Classes (globals.css)
```css
.btn {
  @apply px-4 py-2 rounded-md font-medium transition-colors;
}

.btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700;
}
```

## Error Handling

### Try-Catch Pattern
```typescript
try {
  const result = await api.someOperation();
  // Handle success
} catch (err) {
  setError(getErrorMessage(err));
}
```

### Display Errors
```tsx
{error && (
  <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700">
    {error}
  </div>
)}
```

## Loading States

### Spinner
```tsx
{loading ? (
  <div className="text-center py-12">
    <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-r-transparent"></div>
    <p className="mt-4 text-gray-600">Loading...</p>
  </div>
) : (
  <Content />
)}
```

### Button Loading
```tsx
<button disabled={loading}>
  {loading ? "Saving..." : "Save"}
</button>
```

## TypeScript Types

### Import Types
```typescript
import { Task, TaskCreate, User } from "@/lib/types";
```

### Component Props
```typescript
interface TaskItemProps {
  task: Task;
  onToggle: (taskId: number) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: number) => void;
}

export default function TaskItem({ task, onToggle, onEdit, onDelete }: TaskItemProps) {
  // Component logic
}
```

## Authentication Flow

### Protected Routes
```typescript
"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { getStoredUser } from "@/lib/utils";

export default function ProtectedPage() {
  const router = useRouter();

  useEffect(() => {
    const user = getStoredUser();
    if (!user || !api.isAuthenticated()) {
      router.push("/signin");
    }
  }, [router]);

  // Page content
}
```

### Sign In/Sign Out
```typescript
// Sign in
const response = await api.signin({ email, password });
// Token automatically stored
router.push("/tasks");

// Sign out
api.signout();
// Token automatically cleared
router.push("/");
```

## Environment Variables

### Access in Client Components
```typescript
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

### Required Variables (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=postgresql://...
```

## Best Practices

### Code Organization
- Keep components small and focused
- Extract reusable logic to custom hooks
- Use TypeScript for type safety
- Follow Next.js conventions

### Performance
- Use React.memo for expensive components
- Implement pagination for large lists
- Optimize images with next/image
- Minimize client-side JavaScript

### Accessibility
- Use semantic HTML
- Add proper ARIA labels
- Support keyboard navigation
- Ensure color contrast

### SEO
- Set appropriate metadata
- Use descriptive titles
- Include meta descriptions
- Implement Open Graph tags

## Running the App

### Development
```bash
npm install
npm run dev
# http://localhost:3000
```

### Build
```bash
npm run build
npm start
```

### Linting
```bash
npm run lint
```

## Troubleshooting

### API Connection Issues
- Check `NEXT_PUBLIC_API_URL` is correct
- Ensure backend is running
- Verify CORS configuration

### Authentication Issues
- Clear localStorage and try again
- Check token expiration
- Verify JWT_SECRET matches backend

### Build Errors
- Delete `.next` folder and rebuild
- Check TypeScript errors
- Verify all dependencies are installed

## References

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- API Spec: `@specs/api/rest-endpoints.md`
- Component Patterns: Review existing components in `/components`
