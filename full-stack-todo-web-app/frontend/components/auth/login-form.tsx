'use client';

import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Icons } from '@/components/ui/icons';

interface LoginFormProps {
  onSubmit: (email: string, password: string) => void;
  isLoading: boolean;
  error: string | null;
}

export default function LoginForm({ onSubmit, isLoading, error }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!password) {
      newErrors.password = 'Password is required';
    } else if (password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (validateForm()) {
      onSubmit(email, password);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 max-w-md mx-auto">
      {error && (
        <div className="rounded-md bg-red-900/20 border border-red-500 p-4">
          <div className="text-sm text-red-300">{error}</div>
        </div>
      )}

      <div className="space-y-2">
        <Input
          id="email"
          name="email"
          type="email"
          autoComplete="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email address"
          className={`bg-gray-200 border-0 placeholder:text-gray-500 text-gray-900 ${errors.email ? 'border-red-500' : ''}`}
        />
        {errors.email && (
          <p className="text-sm text-red-400">{errors.email}</p>
        )}
      </div>

      <div className="space-y-2">
        <Input
          id="password"
          name="password"
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          className={`bg-gray-200 border-0 placeholder:text-gray-500 text-gray-900 ${errors.password ? 'border-red-500' : ''}`}
        />
        {errors.password && (
          <p className="text-sm text-red-400">{errors.password}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-blue-500 hover:bg-blue-600 text-white py-4 px-8 text-lg font-semibold rounded-lg shadow-lg transition-all duration-200 disabled:opacity-50"
      >
        {isLoading ? (
          <>
            <Icons.spinner className="inline mr-2 h-4 w-4 animate-spin" />
            Signing in...
          </>
        ) : (
          'Sign In'
        )}
      </button>
    </form>
  );
}