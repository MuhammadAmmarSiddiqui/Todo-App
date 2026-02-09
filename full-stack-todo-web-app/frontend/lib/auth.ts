/**
 * Better Auth Configuration
 *
 * This file configures Better Auth with JWT plugin enabled for secure authentication
 */

import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "your-super-secret-jwt-key-here-make-it-long-and-random",
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
  plugins: [
    jwt({})
  ],
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },
  socialProviders: {
    // Add social providers here if needed
  }
});