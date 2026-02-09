import { NextRequest, NextResponse } from 'next/server';
import * as jose from 'jose';

export async function GET(request: NextRequest) {
  try {
    const authHeader = request.headers.get('Authorization');
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json(
        { message: 'Unauthorized' },
        { status: 401 }
      );
    }

    const token = authHeader.substring(7);
    const secret = new TextEncoder().encode(
      process.env.BETTER_AUTH_SECRET || 'your-super-secret-jwt-key-here-make-it-long-and-random'
    );

    const { payload } = await jose.jwtVerify(token, secret);

    return NextResponse.json({
      id: payload.sub,
      email: payload.email,
    });
  } catch (error) {
    console.error('Auth check error:', error);
    return NextResponse.json(
      { message: 'Invalid token' },
      { status: 401 }
    );
  }
}
