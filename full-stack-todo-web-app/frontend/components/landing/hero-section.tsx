'use client';

import Link from 'next/link';
import { User } from 'lucide-react';

interface HeroSectionProps {
  isAuthenticated: boolean;
  userEmail?: string;
}

export default function HeroSection({ isAuthenticated, userEmail }: HeroSectionProps) {
  return (
    <div className="min-h-screen bg-gray-300 flex flex-col">
      {/* Header */}
      <header className="bg-white py-6 px-6">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-1 h-6 bg-blue-500 rounded-full"></div>
            <h1 className="text-2xl font-bold text-gray-900">TASK MASTER</h1>
          </div>
          <div className="bg-gray-800 rounded-full p-2.5">
            <User className="w-5 h-5 text-white" />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex items-start justify-center px-4 pt-0">
        <div className="w-full max-w-3xl mt-0">
          {isAuthenticated ? (
            <div className="bg-gray-800 rounded-lg shadow-xl p-12 text-center">
              <h2 className="text-4xl font-bold text-white mb-8">
                Welcome back
                <br />
                TASK MASTER
              </h2>
              <p className="text-xl mb-6 text-white">Hello, {userEmail}!</p>
              <Link href="/dashboard/tasks" className="block">
                <button className="w-full max-w-sm mx-auto bg-blue-500 hover:bg-blue-600 text-white py-6 px-8 text-lg font-semibold rounded-lg shadow-lg transition-all duration-200">
                  Go to Dashboard
                </button>
              </Link>
            </div>
          ) : (
            <div className="bg-gray-800 rounded-b-lg shadow-xl p-12 pb-16">
              <h2 className="text-4xl font-bold text-white text-center mb-8">
                Welcome to
                <br />
                TASK MASTER
              </h2>
              
              <div className="space-y-4 max-w-sm mx-auto">
                <Link href="/auth/login" className="block">
                  <button className="w-full bg-blue-500 hover:bg-blue-600 text-white py-6 px-8 text-lg font-semibold rounded-lg shadow-lg transition-all duration-200">
                    Sign In
                  </button>
                </Link>
                <Link href="/auth/register" className="block">
                  <button className="w-full bg-gray-200 hover:bg-gray-300 text-gray-900 py-6 px-8 text-lg font-semibold rounded-lg shadow-lg transition-all duration-200">
                    Register
                  </button>
                </Link>
              </div>

              <p className="text-gray-300 text-center mt-8 text-base">
                Streamline your tasks and boost productivity.
              </p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}