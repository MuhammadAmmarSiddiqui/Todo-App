/**
 * TypeScript Types for Todo Web Application
 *
 * This file defines TypeScript interfaces for all entities used in the application
 */

// User entity type
export interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: Date;
  updatedAt: Date;
}

// Task entity type
export interface Task {
  id: string;
  userId: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
  completedAt?: Date | null;
}

// Session entity type
export interface Session {
  userId: string;
  token: string;
  expiresAt: Date;
  refreshToken?: string;
  createdAt: Date;
}

// DTOs for API requests/responses
export interface TaskRequest {
  title: string;
  description?: string;
  completed?: boolean;
}

export interface TaskResponse extends Task {
  id: string;
  userId: string;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
  completedAt?: Date | null;
}

export interface AuthRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  user: User;
  token: string;
  refreshToken?: string;
}

// API response wrapper types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
}

export interface ApiErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
}

// Hook return types
export interface UseAuthReturn {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => Promise<void>;
  error: string | null;
}

export interface UseTasksReturn {
  tasks: Task[];
  isLoading: boolean;
  createTask: (taskData: TaskRequest) => Promise<Task>;
  updateTask: (id: string, taskData: Partial<TaskRequest>) => Promise<Task>;
  deleteTask: (id: string) => Promise<void>;
  toggleTaskCompletion: (id: string) => Promise<Task>;
  error: string | null;
}

// Chat types
export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system' | 'tool';
  content: string;
  timestamp: Date;
}

export interface ChatConversation {
  id: string;
  title: string;
  createdAt: Date;
  updatedAt: Date;
}