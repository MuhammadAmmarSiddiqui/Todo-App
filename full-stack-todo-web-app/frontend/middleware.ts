import { NextRequest, NextResponse } from 'next/server';

// Protect routes that require authentication
export function middleware(request: NextRequest) {
  // Get the pathname
  const pathname = request.nextUrl.pathname;

  // Define protected routes that require authentication
  const protectedRoutes = ['/dashboard', '/dashboard/tasks'];

  // Check if the current route is protected
  const isProtectedRoute = protectedRoutes.some(route =>
    pathname.startsWith(route)
  );

  // Check for authentication token in cookies/localStorage
  // For Next.js middleware, we can only access cookies, not localStorage
  const token = request.cookies.get('better-auth-session-token')?.value;

  // If user is accessing a protected route but not authenticated
  if (isProtectedRoute && !token) {
    // Redirect to login page
    return NextResponse.redirect(new URL('/auth/login', request.url));
  }

  // Check if user is trying to access login/register pages while authenticated
  const authPages = ['/auth/login', '/auth/register'];
  const isAuthPage = authPages.includes(pathname);

  if (isAuthPage && token) {
    // If user is already logged in, redirect to dashboard
    return NextResponse.redirect(new URL('/dashboard/tasks', request.url));
  }

  // Allow the request to continue
  return NextResponse.next();
}

// Apply middleware to all routes except static assets
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};