'use client';

import React, { createContext, useContext, ReactNode, useState, useEffect } from 'react';
import { User } from '@/types';
import { useAuth } from '@/hooks/use-auth';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => Promise<void>;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const defaultAuthContext: AuthContextType = {
  user: null,
  isLoading: true, // Default to true initially
  isAuthenticated: false,
  login: async () => { throw new Error('AuthProvider not initialized'); },
  register: async () => { throw new Error('AuthProvider not initialized'); },
  logout: async () => { throw new Error('AuthProvider not initialized'); },
  error: null,
};

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [isClient, setIsClient] = useState(false);
  const auth = useAuth();

  useEffect(() => {
    setIsClient(true);
  }, []);

  // Only render the actual auth context after client hydration
  const contextValue = isClient ? auth : defaultAuthContext;

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuthContext() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    // Return default context to prevent runtime errors
    // Functions will throw errors if called outside of provider
    return defaultAuthContext;
  }
  return context;
}