import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { AuthProvider } from '@/components/auth/auth-provider';
import { QueryProvider } from '@/components/providers/query-provider';
import { Suspense } from 'react';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Todo Web Application',
  description: 'A secure multi-user todo application with Better Auth',
  keywords: ['todo', 'productivity', 'task management', 'authentication'],
  authors: [{ name: 'Todo App Team' }],
  creator: 'Todo App Team',
  publisher: 'Todo App Team',
  openGraph: {
    title: 'Todo Web Application',
    description: 'A secure multi-user todo application with Better Auth',
    type: 'website',
    siteName: 'Todo App',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Todo Web Application',
    description: 'A secure multi-user todo application with Better Auth',
  },
  robots: {
    index: true,
    follow: true,
  },
  verification: {
    google: 'google-site-verification-code',
  },
};

import { Toaster } from '@/components/ui/toaster';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <script
          src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
          async
        ></script>
      </head>
      <body className={inter.className}>
        <QueryProvider>
          <Suspense fallback={null}>
            <AuthProvider>
              {children}
              <Toaster />
            </AuthProvider>
          </Suspense>
        </QueryProvider>
      </body>
    </html>
  );
}