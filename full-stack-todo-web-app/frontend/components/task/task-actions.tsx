'use client';

import React from 'react';

interface TaskActionsProps {
  onToggleCompletion: () => void;
  onDelete: () => void;
  isCompleted: boolean;
  isLoading?: boolean;
}

export default function TaskActions({ onToggleCompletion, onDelete, isCompleted, isLoading = false }: TaskActionsProps) {
  return (
    <div className="flex space-x-2">
      <button
        onClick={onToggleCompletion}
        className={`inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded ${
          isCompleted
            ? 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200'
            : 'bg-green-100 text-green-800 hover:bg-green-200'
        }`}
        disabled={isLoading}
      >
        {isCompleted ? 'Mark Pending' : 'Mark Complete'}
      </button>
      <button
        onClick={onDelete}
        className="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded bg-red-100 text-red-800 hover:bg-red-200"
        disabled={isLoading}
      >
        Delete
      </button>
    </div>
  );
}