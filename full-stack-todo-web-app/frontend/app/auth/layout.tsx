import React from 'react';
import { Metadata } from 'next';
import { User } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Authentication | Todo App',
  description: 'Sign in or create an account to access your todo list',
};

interface AuthLayoutProps {
  children: React.ReactNode;
}

export default function AuthLayout({ children }: AuthLayoutProps) {
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
        <div className="w-full max-w-2xl mt-0">
          <div className="bg-gray-800 rounded-b-lg shadow-xl p-12">
            {children}
          </div>
        </div>
      </main>
    </div>
  );
}