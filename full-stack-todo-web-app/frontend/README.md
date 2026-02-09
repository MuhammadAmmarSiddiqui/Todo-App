# Todo Web Application - Frontend

This is the frontend of the Todo Web Application, a modern, responsive web interface built with Next.js 16+ using the App Router. It provides users with an intuitive way to manage their tasks with secure authentication and real-time data synchronization.

## Features

- **User Authentication**: Secure signup, signin, and logout functionality using Better Auth
- **Task Management**: Create, read, update, and delete tasks with optimistic updates
- **Responsive Design**: Fully responsive interface that works on mobile, tablet, and desktop
- **Real-time Updates**: Instant feedback when tasks are modified
- **Secure Token Management**: JWT-based authentication with automatic refresh

## Tech Stack

- **Framework**: Next.js 16+ (App Router)
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth with JWT
- **API Client**: Custom API client with automatic token attachment
- **State Management**: React state management with custom hooks
- **UI Components**: Custom built with Tailwind CSS

## API Integration

The frontend communicates with the backend through REST API endpoints:

| Method | Endpoint                     | Description                           |
|--------|------------------------------|---------------------------------------|
| GET    | /api/{user_id}/tasks         | Retrieve all tasks for the user       |
| POST   | /api/{user_id}/tasks         | Create a new task for the user        |
| GET    | /api/{user_id}/tasks/{id}    | Get details of a specific task        |
| PUT    | /api/{user_id}/tasks/{id}    | Update a specific task                |
| DELETE | /api/{user_id}/tasks/{id}    | Delete a specific task                |
| PATCH  | /api/{user_id}/tasks/{id}/complete | Toggle task completion status    |

## Installation

1. Clone the repository
2. Navigate to the frontend directory
3. Install dependencies:

```bash
npm install
```

4. Set up environment variables:

```bash
cp .env.local.example .env.local
```

5. Update the values in `.env.local` with your configuration

6. Run the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL`: Base URL for the backend API
- `BETTER_AUTH_SECRET`: Secret key for Better Auth
- `BETTER_AUTH_URL`: URL for the Better Auth service

## Security Considerations

- All API requests include JWT tokens in the Authorization header
- User data isolation - each user only sees their own tasks
- Secure token storage using localStorage/sessionStorage
- Proper error handling to prevent information leakage
- Input validation and sanitization

## Folder Structure

```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   └── register/
│   ├── dashboard/
│   │   └── tasks/
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── auth/
│   ├── task/
│   ├── navigation/
│   ├── common/
│   └── ui/
├── lib/
│   ├── auth.ts
│   ├── api-client.ts
│   └── token-storage.ts
├── hooks/
│   ├── use-auth.ts
│   └── use-tasks.ts
├── types/
│   └── index.ts
└── public/
```

## Running Tests

To run the tests:

```bash
npm test
```

## Building for Production

To build the application for production:

```bash
npm run build
```

Then run the production server:

```bash
npm start
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.