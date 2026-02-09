import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    typedRoutes: true,
  },
  env: {
    BETTER_AUTH_URL: process.env.BETTER_AUTH_URL || 'http://localhost:3001',
  },
}

export default nextConfig