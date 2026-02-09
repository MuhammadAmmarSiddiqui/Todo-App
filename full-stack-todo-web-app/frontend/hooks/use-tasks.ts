/**
 * Custom Task Management Hook
 *
 * This hook provides task management functionality using the API client
 */

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api-client';
import { Task, TaskRequest } from '@/types';

interface UseTasksReturn {
  tasks: Task[];
  isLoading: boolean;
  createTask: (taskData: TaskRequest) => Promise<Task>;
  updateTask: (id: string, taskData: Partial<TaskRequest>) => Promise<Task>;
  deleteTask: (id: string) => Promise<void>;
  toggleTaskCompletion: (id: string) => Promise<Task>;
  error: string | null;
}

export const useTasks = (userId: string): UseTasksReturn => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Load tasks on mount and when userId changes
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const fetchedTasks = await apiClient.getUserTasks(userId);
        setTasks(fetchedTasks);
      } catch (err) {
        console.error('Error fetching tasks:', err);
        setError(err instanceof Error ? err.message : 'Failed to load tasks');
      } finally {
        setIsLoading(false);
      }
    };

    if (userId) {
      fetchTasks();
    }
  }, [userId]);

  const createTask = async (taskData: TaskRequest): Promise<Task> => {
    try {
      setError(null);

      const newTask = await apiClient.createTask(userId, taskData);

      // Optimistically update the UI
      setTasks(prev => [...prev, newTask]);

      return newTask;
    } catch (err) {
      console.error('Error creating task:', err);
      setError(err instanceof Error ? err.message : 'Failed to create task');
      throw err;
    }
  };

  const updateTask = async (id: string, taskData: Partial<TaskRequest>): Promise<Task> => {
    try {
      setError(null);

      const updatedTask = await apiClient.updateTask(userId, id, taskData);

      // Optimistically update the UI
      setTasks(prev => prev.map(task => task.id === id ? updatedTask : task));

      return updatedTask;
    } catch (err) {
      console.error('Error updating task:', err);
      setError(err instanceof Error ? err.message : 'Failed to update task');
      throw err;
    }
  };

  const deleteTask = async (id: string): Promise<void> => {
    try {
      setError(null);

      await apiClient.deleteTask(userId, id);

      // Optimistically update the UI
      setTasks(prev => prev.filter(task => task.id !== id));
    } catch (err) {
      console.error('Error deleting task:', err);
      setError(err instanceof Error ? err.message : 'Failed to delete task');
      throw err;
    }
  };

  const toggleTaskCompletion = async (id: string): Promise<Task> => {
    try {
      setError(null);

      const toggledTask = await apiClient.toggleTaskCompletion(userId, id);

      // Optimistically update the UI
      setTasks(prev =>
        prev.map(task =>
          task.id === id ? toggledTask : task
        )
      );

      return toggledTask;
    } catch (err) {
      console.error('Error toggling task completion:', err);
      setError(err instanceof Error ? err.message : 'Failed to toggle task completion');
      throw err;
    }
  };

  return {
    tasks,
    isLoading,
    createTask,
    updateTask,
    deleteTask,
    toggleTaskCompletion,
    error,
  };
};