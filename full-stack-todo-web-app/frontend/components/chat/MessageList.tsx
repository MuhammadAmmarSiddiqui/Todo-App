import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Bot, User, Command, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import { Skeleton } from '@/components/ui/skeleton';
import { ChatMessage } from '@/types';

interface MessageListProps {
  messages: ChatMessage[];
  isLoading?: boolean;
  userInitial?: string;
}

export const MessageList = ({ messages, isLoading, userInitial = 'U' }: MessageListProps) => {
  if (isLoading && messages.length === 0) {
    return (
      <div className="space-y-6 p-4">
        {[...Array(3)].map((_, idx) => (
          <div key={idx} className="flex gap-4 animate-in fade-in slide-in-from-bottom-2 duration-500">
            <Skeleton className="h-8 w-8 rounded-full" />
            <div className="space-y-2 flex-1">
              <Skeleton className="h-4 w-[40%]" />
              <Skeleton className="h-12 w-full rounded-xl" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6 py-4 px-4">
      {messages.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-center">
          <div className="bg-slate-50 p-6 rounded-full mb-4">
            <Bot className="h-12 w-12 text-slate-300" />
          </div>
          <h2 className="text-xl font-bold text-slate-900 mb-2">How can I help you today?</h2>
          <p className="max-w-[280px] text-sm text-slate-500">
            I can help you add tasks, list your agenda, or organize your workspace using natural language.
          </p>
        </div>
      ) : (
        messages.map((message, i) => (
          <div
            key={message.id || i}
            className={`flex gap-3 ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
          >
            <Avatar className="h-8 w-8 shrink-0 border border-slate-100">
              {message.role === 'assistant' ? (
                <AvatarFallback className="bg-indigo-600 text-white">
                  <Bot className="h-4 w-4" />
                </AvatarFallback>
              ) : message.role === 'tool' ? (
                <AvatarFallback className="bg-slate-100 text-slate-600">
                  <Command className="h-4 w-4" />
                </AvatarFallback>
              ) : (
                <AvatarFallback className="bg-slate-200 text-slate-700 font-bold text-xs">
                  {userInitial}
                </AvatarFallback>
              )}
            </Avatar>
            
            <div className={`flex flex-col max-w-[85%] ${message.role === 'user' ? 'items-end' : 'items-start'}`}>
              <div
                className={`px-4 py-2 rounded-xl text-sm leading-relaxed ${
                  message.role === 'user'
                    ? 'bg-indigo-600 text-white'
                    : message.role === 'tool'
                    ? 'bg-slate-50 text-slate-500 border border-slate-100 font-mono text-[10px]'
                    : 'bg-slate-100 text-slate-800 border border-slate-200'
                }`}
              >
                {message.role === 'tool' ? (
                  <div className="flex items-start gap-2">
                    <CheckCircle2 className="h-3 w-3 mt-0.5 text-emerald-500" />
                    <p className="whitespace-pre-wrap">{message.content}</p>
                  </div>
                ) : (
                  <p className="whitespace-pre-wrap">{message.content}</p>
                )}
              </div>
              <span className="text-[9px] text-slate-400 mt-1 uppercase font-bold tracking-tighter">
                {new Date(message.timestamp || Date.now()).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
          </div>
        ))
      )}
      
      {isLoading && messages.length > 0 && (
        <div className="flex gap-3 animate-in fade-in duration-300">
          <Avatar className="h-8 w-8 shrink-0 border border-slate-100">
            <AvatarFallback className="bg-indigo-600 text-white">
               <Loader2 className="h-4 w-4 animate-spin" />
            </AvatarFallback>
          </Avatar>
          <div className="bg-slate-100 text-slate-400 px-4 py-2 rounded-xl text-xs font-bold animate-pulse flex items-center">
             AI is thinking...
          </div>
        </div>
      )}
    </div>
  );
};