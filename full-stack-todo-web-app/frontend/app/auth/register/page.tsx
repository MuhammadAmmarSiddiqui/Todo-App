'use client';

import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';
import RegisterForm from '@/components/auth/register-form';

export default function RegisterPage() {
  const router = useRouter();
  const { register, error, isLoading } = useAuth();

  const handleRegister = async (email: string, password: string, name?: string) => {
    try {
      await register(email, password, name);
      router.push('/dashboard/tasks');
      router.refresh();
    } catch (err) {
      console.error('Registration failed:', err);
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold text-white text-center">Create your account</h2>
      <RegisterForm onSubmit={handleRegister} isLoading={isLoading} error={error} />
      <div className="text-center text-white">
        Already a user?{' '}
        <Link href="/auth/login" className="text-blue-400 hover:text-blue-300 font-semibold">
          Sign In
        </Link>
      </div>
    </div>
  );
}