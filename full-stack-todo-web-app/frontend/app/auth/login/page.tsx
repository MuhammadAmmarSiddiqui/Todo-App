'use client';

import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';
import LoginForm from '@/components/auth/login-form';

export default function LoginPage() {
  const router = useRouter();
  const { login, error, isLoading } = useAuth();

  const handleLogin = async (email: string, password: string) => {
    try {
      await login(email, password);
      router.push('/dashboard/tasks');
      router.refresh();
    } catch (err) {
      console.error('Login failed:', err);
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold text-white text-center">Sign In to your account</h2>
      <LoginForm onSubmit={handleLogin} isLoading={isLoading} error={error} />
      <div className="text-center">
        <Link href="/auth/register" className="inline-block px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-900 font-semibold rounded-lg transition-all duration-200">
          Register
        </Link>
      </div>
    </div>
  );
}