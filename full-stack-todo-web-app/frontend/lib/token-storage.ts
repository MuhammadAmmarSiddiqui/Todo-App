/**
 * JWT Token Storage and Retrieval Utilities
 *
 * This module handles storing, retrieving, and managing JWT tokens in the frontend.
 */

/**
 * Get JWT token from storage
 * @returns JWT token string or null if not found
 */
export const getJwtToken = (): string | null => {
  if (typeof window !== 'undefined') {
    // Try to get from localStorage first
    let token = localStorage.getItem('better-auth-session-token');

    if (!token) {
      // Try to get from sessionStorage
      token = sessionStorage.getItem('better-auth-session-token');
    }

    if (!token) {
      // Try to get from cookies (set by API routes)
      const cookies = document.cookie.split(';');
      for (const cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'better-auth-session-token') {
          token = decodeURIComponent(value);
          // Sync to localStorage for consistency
          if (token) {
            localStorage.setItem('better-auth-session-token', token);
          }
          break;
        }
      }
    }

    return token;
  }
  return null;
};

/**
 * Store JWT token in storage
 * @param token - JWT token string to store
 * @param remember - Whether to persist beyond session (defaults to false)
 */
export const setJwtToken = (token: string, remember: boolean = false): void => {
  if (typeof window !== 'undefined') {
    if (remember) {
      // Store in localStorage for persistence across sessions
      localStorage.setItem('better-auth-session-token', token);
    } else {
      // Store in sessionStorage for current session only
      sessionStorage.setItem('better-auth-session-token', token);
    }
  }
};

/**
 * Remove JWT token from storage
 */
export const removeJwtToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('better-auth-session-token');
    sessionStorage.removeItem('better-auth-session-token');
  }
};

/**
 * Get token expiration information
 * @returns Object with expiration timestamp and whether token is expired
 */
export const getTokenExpirationInfo = (): {
  exp: number | null;
  isExpired: boolean;
  timeUntilExpiry: number | null
} => {
  const token = getJwtToken();

  if (!token) {
    return { exp: null, isExpired: true, timeUntilExpiry: null };
  }

  try {
    // Split the token to get the payload
    const parts = token.split('.');
    if (parts.length !== 3) {
      throw new Error('Invalid token format');
    }

    // Decode the payload (second part)
    const payload = JSON.parse(atob(parts[1]));

    if (!payload.exp) {
      return { exp: null, isExpired: false, timeUntilExpiry: null };
    }

    const expTimestamp = payload.exp;
    const currentTime = Math.floor(Date.now() / 1000);
    const isExpired = currentTime >= expTimestamp;
    const timeUntilExpiry = isExpired ? null : expTimestamp - currentTime;

    return {
      exp: expTimestamp,
      isExpired,
      timeUntilExpiry
    };
  } catch (error) {
    console.error('Error decoding token:', error);
    return { exp: null, isExpired: true, timeUntilExpiry: null };
  }
};

/**
 * Check if the current token is expired
 * @returns Boolean indicating if token is expired
 */
export const isTokenExpired = (): boolean => {
  return getTokenExpirationInfo().isExpired;
};

/**
 * Get user ID from token
 * @returns User ID string or null if not found
 */
export const getUserIdFromToken = (): string | null => {
  const token = getJwtToken();

  if (!token) {
    return null;
  }

  try {
    // Split the token to get the payload
    const parts = token.split('.');
    if (parts.length !== 3) {
      throw new Error('Invalid token format');
    }

    // Decode the payload (second part)
    const payload = JSON.parse(atob(parts[1]));

    // Better Auth typically stores user ID in 'sub' (subject) field
    return payload.sub || null;
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};

/**
 * Refresh JWT token using refresh token
 * @returns New access token or null if refresh fails
 */
export const refreshJwtToken = async (): Promise<string | null> => {
  if (typeof window === 'undefined') {
    return null;
  }

  try {
    const refreshToken = localStorage.getItem('better-auth-refresh-token');

    if (!refreshToken) {
      return null;
    }

    const response = await fetch('/api/auth/refresh', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${refreshToken}`,
      },
    });

    if (!response.ok) {
      // If refresh fails, remove the invalid refresh token
      localStorage.removeItem('better-auth-refresh-token');
      return null;
    }

    const data = await response.json();

    if (data.token) {
      // Store the new token
      setJwtToken(data.token, true);

      // Store the new refresh token if provided
      if (data.refreshToken) {
        localStorage.setItem('better-auth-refresh-token', data.refreshToken);
      }

      return data.token;
    }

    return null;
  } catch (error) {
    console.error('Error refreshing token:', error);
    localStorage.removeItem('better-auth-refresh-token');
    return null;
  }
};