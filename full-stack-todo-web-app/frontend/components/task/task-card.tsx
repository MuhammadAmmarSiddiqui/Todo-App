'use client';

import React from 'react';
import { Task } from '@/types';

interface TaskCardProps {
  task: Task;
  onToggleCompletion: (id: string) => void;
  onDelete: (id: string) => void;
  onEdit: (task: Task) => void;
  isLoading?: boolean;
}

export default function TaskCard({ task, onToggleCompletion, onDelete, onEdit, isLoading = false }: TaskCardProps) {
  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
      <div className="px-4 py-5 sm:px-6">
        <div className="flex items-center justify-between">
          <h3 className={`text-lg leading-6 font-medium ${
            task.completed ? 'text-gray-400 line-through' : 'text-gray-900'
          }`}>
            {task.title}
          </h3>
          <span className={`inline-flex px-2 py-1 text-xs leading-4 rounded-full ${
            task.completed
              ? 'bg-green-100 text-green-800'
              : 'bg-yellow-100 text-yellow-800'
          }`}>
            {task.completed ? 'Completed' : 'Pending'}
          </span>
        </div>
        {task.description && (
          <div className="mt-2 text-sm text-gray-500">
            <p>{task.description}</p>
          </div>
        )}
      </div>
      <div className="bg-gray-50 px-4 py-4 sm:px-6">
        <div className="flex justify-between">
          <div className="text-xs text-gray-500">
            Created: {new Date(task.createdAt).toLocaleDateString()}
          </div>
          <div className="flex space-x-2">
            <button
              onClick={() => onEdit(task)}
              className="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded bg-blue-100 text-blue-800 hover:bg-blue-200"
              disabled={isLoading}
            >
              Edit
            </button>
            <button
              onClick={() => onToggleCompletion(task.id)}
              className={`inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded ${
                task.completed
                  ? 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'
                  : 'bg-green-100 text-green-800 hover:bg-green-200'
              }`}
              disabled={isLoading}
            >
              {task.completed ? 'Mark Pending' : 'Mark Complete'}
            </button>
            <button
              onClick={() => onDelete(task.id)}
              className="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded bg-red-100 text-red-800 hover:bg-red-200"
              disabled={isLoading}
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}