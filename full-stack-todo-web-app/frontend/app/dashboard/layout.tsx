import React from 'react';
import { Metadata } from 'next';
import Navbar from '@/components/navigation/navbar';

export const metadata: Metadata = {
  title: 'Dashboard | Todo App',
  description: 'Manage your tasks and productivity',
};

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main>
        {children}
      </main>
    </div>
  );
}