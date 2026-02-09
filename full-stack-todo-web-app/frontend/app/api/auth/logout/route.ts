import { NextResponse } from 'next/server';

export async function POST() {
  // Create response
  const res = NextResponse.json({ message: 'Logged out successfully' });
  
  // Clear the auth cookie
  res.cookies.set('better-auth-session-token', '', {
    httpOnly: false,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    path: '/',
    maxAge: 0, // Expire immediately
  });

  return res;
}
