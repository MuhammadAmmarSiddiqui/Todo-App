'use client';

import React from 'react';
import Link from 'next/link';
import { useAuthContext } from '@/components/auth/auth-provider';

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuthContext();

  const handleLogout = async () => {
    try {
      await logout();
      // Redirect to login page after logout
      window.location.href = '/auth/login';
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <nav className="bg-indigo-600" role="navigation" aria-label="Main navigation">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Link href={"/dashboard" as any} className="text-white text-xl font-bold" aria-label="Todo App Home">
                Todo App
              </Link>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <Link
                  href={"/dashboard/tasks"}
                  className="text-white hover:bg-indigo-700 px-3 py-2 rounded-md text-sm font-medium"
                  aria-current="page"
                >
                  My Tasks
                </Link>
              </div>
            </div>
          </div>
          <div className="hidden md:block">
            <div className="ml-4 flex items-center md:ml-6">
              {isAuthenticated && user ? (
                <div className="flex items-center space-x-4">
                  <span className="text-white text-sm hidden md:inline-block" aria-label={`Welcome, ${user.name || user.email}`}>
                    Welcome, {user.name || user.email}
                  </span>
                  <button
                    onClick={handleLogout}
                    className="text-white bg-indigo-700 hover:bg-indigo-800 px-3 py-2 rounded-md text-sm font-medium"
                    aria-label="Logout"
                  >
                    Logout
                  </button>
                </div>
              ) : (
                <Link
                  href={"/auth/login" as any}
                  className="text-white hover:bg-indigo-700 px-3 py-2 rounded-md text-sm font-medium"
                  aria-label="Login"
                >
                  Login
                </Link>
              )}
            </div>
          </div>
          <div className="-mr-2 flex md:hidden">
            {/* Mobile menu button */}
            <button
              type="button"
              className="bg-indigo-600 inline-flex items-center justify-center p-2 rounded-md text-white hover:text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-indigo-600 focus:ring-white"
              aria-controls="mobile-menu"
              aria-expanded="false"
              aria-label="Main menu"
            >
              <span className="sr-only">Open main menu</span>
              {/* Icon when menu is closed */}
              <svg
                className="block h-6 w-6"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu, show/hide based on menu state */}
      <div className="md:hidden" id="mobile-menu" role="menu" aria-orientation="vertical">
        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
          <Link
            href={"/dashboard/tasks"}
            className="text-white hover:bg-indigo-700 block px-3 py-2 rounded-md text-base font-medium"
            role="menuitem"
          >
            My Tasks
          </Link>
          {isAuthenticated && user ? (
            <div className="space-y-1">
              <div className="text-white px-3 py-2 rounded-md text-base font-medium" role="menuitem">
                Welcome, {user.name || user.email}
              </div>
              <button
                onClick={handleLogout}
                className="text-white hover:bg-indigo-700 block w-full text-left px-3 py-2 rounded-md text-base font-medium"
                role="menuitem"
                aria-label="Logout"
              >
                Logout
              </button>
            </div>
          ) : (
            <Link
              href={"/auth/login" as any}
              className="text-white hover:bg-indigo-700 block px-3 py-2 rounded-md text-base font-medium"
              role="menuitem"
            >
              Login
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}