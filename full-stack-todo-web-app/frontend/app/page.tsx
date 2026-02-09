'use client';

import { useAuthContext } from '@/components/auth/auth-provider';
import HeroSection from '@/components/landing/hero-section';

export default function HomePage() {
  const { user, isAuthenticated, isLoading } = useAuthContext();

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <HeroSection 
      isAuthenticated={isAuthenticated} 
      userEmail={user?.email} 
    />
  );
}