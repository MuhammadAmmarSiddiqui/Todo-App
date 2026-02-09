# Quickstart Guide: Frontend Development & Full Integration

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Access to the backend API (assumes running on localhost:8000)
- BETTER_AUTH_SECRET environment variable set

## Setup Instructions

### 1. Clone and Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

Required dependencies include:
- next (v16+)
- react and react-dom
- typescript
- tailwindcss
- better-auth
- @tanstack/react-query
- lucide-react
- clsx
- tailwind-merge
- @radix-ui/react-* (for shadcn/ui components)

### 3. Environment Configuration
Create a `.env.local` file in the frontend directory:

```env
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
BETTER_AUTH_SECRET=your_jwt_secret_key
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### 4. Run Development Server
```bash
npm run dev
# or
yarn dev
```

Application will be available at `http://localhost:3000`

## Key Commands

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter
- `npm run test` - Run tests

## Project Structure Overview

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Authentication routes
│   ├── dashboard/         # Protected dashboard routes
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # Reusable React components
│   ├── ui/               # Shadcn/ui components
│   ├── auth/             # Authentication components
│   └── task/             # Task management components
├── lib/                  # Utility functions and API client
├── hooks/                # Custom React hooks
└── public/               # Static assets
```

## Running Tests

Unit tests:
```bash
npm run test:unit
```

Integration tests:
```bash
npm run test:integration
```

End-to-end tests:
```bash
npm run test:e2e
```

## API Integration

The frontend connects to the backend API at `/api/{user_id}/tasks` endpoints. The API client automatically:
- Attaches JWT tokens from Better Auth session
- Handles authentication errors
- Provides proper error messaging
- Implements retry logic for failed requests

## Authentication Flow

1. User visits `/login` or `/register`
2. Better Auth manages the authentication flow
3. JWT tokens are stored securely
4. API requests automatically include authorization headers
5. Protected routes check for valid session before rendering