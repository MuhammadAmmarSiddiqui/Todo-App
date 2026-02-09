'use client';

import { useState, useEffect } from 'react';
import { useAuthContext } from '@/components/auth/auth-provider';
import { useTasks } from '@/hooks/use-tasks';
import { Task, TaskRequest } from '@/types';
import TaskList from '@/components/task/task-list';
import TaskForm from '@/components/task/task-form';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Icons } from '@/components/ui/icons';
import { User, LogOut, CheckCircle, Clock, ListTodo, Sparkles } from 'lucide-react';
import { ChatInterface } from '@/components/chat/ChatInterface';

export default function TasksDashboard() {
  const { user, isLoading: authLoading, isAuthenticated, logout } = useAuthContext();
  const { tasks, isLoading: tasksLoading, createTask, updateTask, deleteTask, toggleTaskCompletion, error: tasksError } = useTasks(user?.id || '');
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  useEffect(() => {
    if (!isAuthenticated && !authLoading) {
      window.location.href = '/auth/login';
    }
  }, [isAuthenticated, authLoading]);

  const handleCreateTask = async (taskData: TaskRequest) => {
    try {
      await createTask(taskData);
      setShowForm(false);
    } catch (error) {
      console.error('Failed to create task:', error);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowForm(false);
  };

  const handleUpdateTask = async (taskData: TaskRequest) => {
    if (!editingTask) return;
    try {
      await updateTask(editingTask.id, {
        title: taskData.title,
        description: taskData.description,
      });
      setEditingTask(null);
    } catch (error) {
      console.error('Failed to update task:', error);
    }
  };

  const handleCancelEdit = () => {
    setEditingTask(null);
  };

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="flex flex-col items-center gap-4 animate-in fade-in zoom-in duration-500">
          <div className="h-12 w-12 rounded-2xl bg-primary/10 flex items-center justify-center border border-primary/20">
            <Icons.spinner className="h-6 w-6 text-primary animate-spin" />
          </div>
          <p className="text-muted-foreground font-medium animate-pulse">Initializing FocusFlow Workspace...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) return null;

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Standard Header */}
      <nav className="bg-white border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Sparkles className="h-6 w-6 text-indigo-600 mr-2" />
              <span className="text-xl font-bold text-slate-900">FocusFlow</span>
            </div>
            <div className="flex items-center gap-4">
              <span className="hidden md:block text-sm text-slate-600">{user?.name || user?.email}</span>
              <Button onClick={logout} variant="ghost" size="sm" className="flex items-center gap-2">
                <LogOut className="h-4 w-4" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Dashboard */}
      <main className="flex-1 max-w-7xl w-full mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-slate-500 uppercase tracking-wider">Total Tasks</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{tasks.length}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-slate-500 uppercase tracking-wider">Completed</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{tasks.filter(t => t.completed).length}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-slate-500 uppercase tracking-wider">Pending</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{tasks.filter(t => !t.completed).length}</div>
            </CardContent>
          </Card>
        </div>

        <div className="flex justify-between items-center bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <div>
            <h2 className="text-lg font-bold text-slate-900">Manage Your Tasks</h2>
            <p className="text-sm text-slate-500">Create and organize your daily agenda.</p>
          </div>
          <Button onClick={() => setShowForm(true)} className="bg-indigo-600 hover:bg-indigo-700">
            Create Task
          </Button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Task List Section */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden h-[600px] flex flex-col">
            <div className="px-6 py-4 border-b border-slate-100 bg-slate-50">
              <h3 className="font-bold text-slate-900">Task Agenda</h3>
            </div>
            <ScrollArea className="flex-1">
              <div className="p-4">
                <TaskList
                  tasks={tasks}
                  onToggleCompletion={toggleTaskCompletion}
                  onDelete={deleteTask}
                  onEdit={handleEditTask}
                  isLoading={tasksLoading}
                />
              </div>
            </ScrollArea>
          </div>

          {/* Chat Assistant Section */}
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden h-[600px]">
            <ChatInterface />
          </div>
        </div>

        {/* Dialogs */}
        <Dialog open={showForm || !!editingTask} onOpenChange={(open) => { if (!open) { setShowForm(false); setEditingTask(null); } }}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>{editingTask ? 'Edit Task' : 'Create Task'}</DialogTitle>
            </DialogHeader>
            <TaskForm
              onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
              isLoading={tasksLoading}
              error={tasksError}
              submitButtonText={editingTask ? "Update" : "Create"}
              onCancel={() => { setShowForm(false); setEditingTask(null); }}
              initialData={editingTask ? {
                title: editingTask.title,
                description: editingTask.description || '',
              } : undefined}
            />
          </DialogContent>
        </Dialog>
      </main>
    </div>
  );
}