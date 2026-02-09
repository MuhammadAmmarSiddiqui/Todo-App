'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuthContext } from '@/components/auth/auth-provider';
import { useTasks } from '@/hooks/use-tasks';
import { Task } from '@/types';
import LoadingSpinner from '@/components/common/loading-spinner';
import TaskForm from '@/components/task/task-form';

export default function IndividualTaskPage() {
  const params = useParams();
  const router = useRouter();
  const taskId = params.id as string;
  const { user, isAuthenticated } = useAuthContext();
  const { tasks, isLoading, updateTask, deleteTask, error } = useTasks(user?.id || '');
  const [editing, setEditing] = useState(false);
  const [updatedTask, setUpdatedTask] = useState<Task | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/auth/login' as any);
    }
  }, [isAuthenticated, router]);

  useEffect(() => {
    if (tasks.length > 0) {
      const task = tasks.find(t => t.id === taskId);
      if (task) {
        setUpdatedTask(task);
      } else {
        // Task not found, redirect to tasks list
        router.push('/dashboard/tasks' as any);
      }
    }
  }, [tasks, taskId, router]);

  const handleUpdateTask = async (taskData: { title?: string; description?: string; completed?: boolean }) => {
    try {
      if (!updatedTask) return;

      const updated = await updateTask(updatedTask.id, taskData);
      setUpdatedTask(updated);
      setEditing(false);
    } catch (err) {
      console.error('Failed to update task:', err);
    }
  };

  const handleDeleteTask = async () => {
    if (!updatedTask) return;

    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(updatedTask.id);
        router.push('/dashboard/tasks' as any);
      } catch (err) {
        console.error('Failed to delete task:', err);
      }
    }
  };

  const handleToggleCompletion = async () => {
    if (!updatedTask) return;

    try {
      const updated = await updateTask(updatedTask.id, { completed: !updatedTask.completed });
      setUpdatedTask(updated);
    } catch (err) {
      console.error('Failed to toggle task completion:', err);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" centered />
      </div>
    );
  }

  if (!updatedTask) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Task not found</h2>
          <button
            onClick={() => router.push('/dashboard/tasks')}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Back to Tasks
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <h2 className="text-lg leading-6 font-medium text-gray-900">
                Task Details
              </h2>
              <button
                onClick={() => router.back()}
                className="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Back
              </button>
            </div>
          </div>

          <div className="px-4 py-5 sm:p-6">
            {error && (
              <div className="mb-4 rounded-md bg-red-50 p-4">
                <div className="text-sm text-red-700">{error}</div>
              </div>
            )}

            {editing ? (
              <div>
                <h3 className="text-md font-medium text-gray-900 mb-4">Edit Task</h3>
                <TaskForm
                  onSubmit={(taskData) => handleUpdateTask(taskData)}
                  isLoading={isLoading}
                  error={error}
                  submitButtonText="Save Changes"
                  onCancel={() => setEditing(false)}
                />
              </div>
            ) : (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-medium text-gray-900">{updatedTask.title}</h3>
                  <div className="mt-2 flex items-center">
                    <span className={`inline-flex px-2 py-1 text-xs leading-4 rounded-full ${
                      updatedTask.completed
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {updatedTask.completed ? 'Completed' : 'Pending'}
                    </span>
                    <span className="ml-2 text-xs text-gray-500">
                      Created: {new Date(updatedTask.createdAt).toLocaleDateString()}
                    </span>
                    {updatedTask.completedAt && (
                      <span className="ml-2 text-xs text-gray-500">
                        Completed: {new Date(updatedTask.completedAt).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                </div>

                {updatedTask.description && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Description</dt>
                    <dd className="mt-1 text-sm text-gray-900">{updatedTask.description}</dd>
                  </div>
                )}

                <div className="flex space-x-3">
                  <button
                    onClick={handleToggleCompletion}
                    className={`inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded ${
                      updatedTask.completed
                        ? 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'
                        : 'bg-green-100 text-green-800 hover:bg-green-200'
                    }`}
                  >
                    {updatedTask.completed ? 'Mark Pending' : 'Mark Complete'}
                  </button>

                  <button
                    onClick={() => setEditing(true)}
                    className="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded text-gray-700 bg-white hover:bg-gray-50"
                  >
                    Edit
                  </button>

                  <button
                    onClick={handleDeleteTask}
                    className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded bg-red-100 text-red-800 hover:bg-red-200"
                  >
                    Delete
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}