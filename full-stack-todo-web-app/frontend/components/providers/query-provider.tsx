'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactNode } from 'react';

// Create a single instance of QueryClient
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Default cache time of 5 minutes
      gcTime: 5 * 60 * 1000, // 5 minutes in milliseconds
      // Refetch on window focus disabled by default
      refetchOnWindowFocus: false,
      // Retry failed queries once
      retry: 1,
    },
  },
});

interface QueryProviderProps {
  children: ReactNode;
}

export function QueryProvider({ children }: QueryProviderProps) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}