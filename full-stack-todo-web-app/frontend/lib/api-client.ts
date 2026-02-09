/**
 * API Client for Todo Web Application
 *
 * This module provides functions to interact with the FastAPI backend,
 * automatically including JWT tokens in requests for authentication.
 */

import { getJwtToken, refreshJwtToken } from "./token-storage";

interface ApiRequestOptions {
  method?: "GET" | "POST" | "PUT" | "DELETE" | "PATCH";
  headers?: Record<string, string>;
  body?: any;
}

class ApiClient {
  private baseUrl: string;

  constructor(
    baseUrl: string = process.env.NEXT_PUBLIC_API_BASE_URL ||
      "http://localhost:8000",
  ) {
    this.baseUrl = baseUrl;
  }

  private async makeRequest<T>(
    endpoint: string,
    options: ApiRequestOptions = {},
    retries = 3,
  ): Promise<T> {
    const { method = "GET", headers = {}, body } = options;

    // Get the JWT token from auth utilities
    let token = getJwtToken();

    // Construct the full URL
    const url = `${this.baseUrl}${endpoint}`;

    // Prepare headers
    const requestHeaders: Record<string, string> = {
      "Content-Type": "application/json",
      ...headers,
    };

    // Add Authorization header if token is available
    if (token) {
      requestHeaders["Authorization"] = `Bearer ${token}`;
    }

    // Prepare request body
    let requestBody: string | undefined;
    if (body && typeof body === "object") {
      requestBody = JSON.stringify(body);
    } else if (body && typeof body === "string") {
      requestBody = body;
    }

    let lastError: Error | null = null;

    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        let response = await fetch(url, {
          method,
          headers: requestHeaders,
          body: requestBody,
        });

        // If we get a 401, try to refresh the token and retry the request
        if (response.status === 401) {
          const newToken = await refreshJwtToken();

          if (newToken) {
            // Retry the request with the new token
            requestHeaders["Authorization"] = `Bearer ${newToken}`;

            response = await fetch(url, {
              method,
              headers: requestHeaders,
              body: requestBody,
            });
          }
        }

        // Handle different response status codes
        if (!response.ok) {
          if (response.status === 401) {
            throw new Error("Unauthorized: Invalid or expired token");
          } else if (response.status === 403) {
            throw new Error("Forbidden: Insufficient permissions");
          } else if (response.status === 404) {
            throw new Error("Not Found: Resource does not exist");
          } else {
            const errorText = await response.text();
            throw new Error(`API Error: ${response.status} - ${errorText}`);
          }
        }

        // Handle responses without body (e.g., DELETE requests)
        if (
          response.status === 204 ||
          response.headers.get("content-length") === "0"
        ) {
          return undefined as unknown as T;
        }

        // Parse JSON response
        const data = await response.json();
        return data;
      } catch (error) {
        lastError = error as Error;

        // If this was the last attempt, throw the error
        if (attempt === retries) {
          break;
        }

        // Network error or other transient error, wait before retrying
        if (
          error instanceof TypeError ||
          (error instanceof Error && error.message.includes("fetch"))
        ) {
          // Exponential backoff: wait 1s, 2s, 4s, etc.
          const delay = Math.pow(2, attempt) * 1000;
          console.warn(
            `Request failed, retrying in ${delay}ms... (attempt ${attempt + 1}/${retries + 1})`,
          );
          await new Promise((resolve) => setTimeout(resolve, delay));
        } else {
          // Non-retryable error, don't retry
          break;
        }
      }
    }

    // If we get here, all retries have been exhausted
    if (lastError) {
      console.error(
        `API request failed after ${retries + 1} attempts: ${lastError.message}`,
      );
      throw lastError;
    } else {
      throw new Error("API request failed after retries");
    }
  }

  // Task-related API methods
  getUserTasks = async (userId: string): Promise<any[]> => {
    return this.makeRequest(`/api/${userId}/tasks`, {
      method: "GET",
    });
  }

  createTask = async (
    userId: string,
    taskData: { title: string; description?: string; completed?: boolean },
  ): Promise<any> => {
    return this.makeRequest(`/api/${userId}/tasks`, {
      method: "POST",
      body: {
        ...taskData,
        user_id: parseInt(userId, 10), // Add required user_id as integer
        completed: taskData.completed ?? false,
      },
    });
  }

  getTaskById = async (userId: string, taskId: string): Promise<any> => {
    return this.makeRequest(`/api/${userId}/tasks/${taskId}`, {
      method: "GET",
    });
  }

  updateTask = async (
    userId: string,
    taskId: string,
    taskData: Partial<{
      title: string;
      description?: string;
      is_completed?: boolean;
    }>,
  ): Promise<any> => {
    return this.makeRequest(`/api/${userId}/tasks/${taskId}`, {
      method: "PUT",
      body: taskData,
    });
  }

  deleteTask = async (userId: string, taskId: string): Promise<void> => {
    await this.makeRequest(`/api/${userId}/tasks/${taskId}`, {
      method: "DELETE",
    });
  }

  toggleTaskCompletion = async (userId: string, taskId: string): Promise<any> => {
    return this.makeRequest(`/api/${userId}/tasks/${taskId}/complete`, {
      method: "PATCH",
    });
  }

  // Chat-related API methods
  getUserConversations = async (userId: string): Promise<any> => {
    return this.makeRequest(`/api/chat/${userId}/conversations`, {
      method: "GET",
    });
  }

  getConversationDetail = async (userId: string, conversationId: string): Promise<any> => {
    return this.makeRequest(`/api/chat/${userId}/conversation/${conversationId}`, {
      method: "GET",
    });
  }

  sendChatMessage = async (userId: string, message: string, conversationId?: string): Promise<any> => {
    return this.makeRequest(`/api/chat/${userId}/`, {
      method: "POST",
      body: {
        message,
        conversation_id: conversationId,
      },
    });
  }

  deleteConversation = async (userId: string, conversationId: string): Promise<any> => {
    return this.makeRequest(`/api/chat/${userId}/conversation/${conversationId}`, {
      method: "DELETE",
    });
  }
}

// Create a singleton instance of the API client
export const apiClient = new ApiClient();

// Export individual methods for convenience
export const {
  getUserTasks,
  createTask,
  getTaskById,
  updateTask,
  deleteTask,
  toggleTaskCompletion,
  getUserConversations,
  getConversationDetail,
  sendChatMessage,
  deleteConversation: deleteChatConversation,
} = apiClient;
