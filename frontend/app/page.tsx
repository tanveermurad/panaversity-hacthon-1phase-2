import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-md w-full p-8 bg-white rounded-2xl shadow-xl">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Todo App
          </h1>
          <p className="text-gray-600 mb-8">
            Manage your tasks efficiently
          </p>

          <div className="space-y-4">
            <Link
              href="/signin"
              className="block w-full btn btn-primary text-center"
            >
              Sign In
            </Link>

            <Link
              href="/signup"
              className="block w-full btn btn-secondary text-center"
            >
              Sign Up
            </Link>
          </div>

          <div className="mt-8 pt-6 border-t border-gray-200">
            <p className="text-sm text-gray-500">
              Built with Next.js 16+, FastAPI, and Neon PostgreSQL
            </p>
            <p className="text-xs text-gray-400 mt-2">
              Hackathon Phase II Challenge
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
