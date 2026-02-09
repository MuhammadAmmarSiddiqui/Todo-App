/**
 * Custom Authentication Hook
 *
 * This hook provides authentication functionality using Better Auth
 */

import { useState, useEffect } from 'react';
import { auth } from '@/lib/auth';
import { User } from '@/types';
import { getJwtToken, setJwtToken, removeJwtToken } from '@/lib/token-storage';

interface UseAuthReturn {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => Promise<void>;
  error: string | null;
}

export const useAuth = (): UseAuthReturn => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Check session on mount
  useEffect(() => {
    const checkSession = async () => {
      try {
        setIsLoading(true);
        const token = getJwtToken();

        if (token) {
          // Verify token and get user info
          // In a real implementation, you'd decode the JWT or make an API call to verify
          // For now, we'll assume the token is valid and try to get user info
          const response = await fetch('/api/auth/me', {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });

          if (response.ok) {
            const userData = await response.json();
            setUser(userData);
            setIsAuthenticated(true);
          } else {
            // Token is invalid/expired, remove it
            removeJwtToken();
            setIsAuthenticated(false);
          }
        }
      } catch (err) {
        console.error('Error checking session:', err);
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setIsLoading(false);
      }
    };

    checkSession();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setError(null);

      // Call Better Auth login API
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Login failed');
      }

      const data = await response.json();

      // Store the token
      if (data.token) {
        setJwtToken(data.token, true); // Remember user
      }

      // Update state
      setUser(data.user);
      setIsAuthenticated(true);
    } catch (err) {
      console.error('Login error:', err);
      setError(err instanceof Error ? err.message : 'Login failed');
      throw err;
    }
  };

  const register = async (email: string, password: string, name?: string) => {
    try {
      setError(null);

      // Call Better Auth register API
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Registration failed');
      }

      const data = await response.json();

      // Store the token
      if (data.token) {
        setJwtToken(data.token, true); // Remember user
      }

      // Update state
      setUser(data.user);
      setIsAuthenticated(true);
    } catch (err) {
      console.error('Registration error:', err);
      setError(err instanceof Error ? err.message : 'Registration failed');
      throw err;
    }
  };

  const logout = async () => {
    try {
      setError(null);

      // Call Better Auth logout API
      await fetch('/api/auth/logout', {
        method: 'POST',
      });

      // Remove token from storage
      removeJwtToken();

      // Update state
      setUser(null);
      setIsAuthenticated(false);
    } catch (err) {
      console.error('Logout error:', err);
      setError(err instanceof Error ? err.message : 'Logout failed');
    }
  };

  return {
    user,
    isLoading,
    isAuthenticated,
    login,
    register,
    logout,
    error,
  };
};