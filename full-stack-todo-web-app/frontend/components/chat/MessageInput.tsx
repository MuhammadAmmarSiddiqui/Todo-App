import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Send, Sparkles } from 'lucide-react';

interface MessageInputProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSubmit: (e: React.FormEvent) => void;
  disabled?: boolean;
}

export const MessageInput = ({ value, onChange, onSubmit, disabled }: MessageInputProps) => {
  return (
    <form onSubmit={onSubmit} className="flex gap-2">
      <div className="flex-1 flex gap-2 bg-white border border-slate-200 px-3 py-1.5 rounded-xl shadow-sm focus-within:border-indigo-500 transition-colors">
        <Input
          value={value}
          onChange={onChange}
          placeholder="Ask AI to manage your tasks..."
          disabled={disabled}
          className="flex-1 border-none bg-transparent focus-visible:ring-0 shadow-none text-sm placeholder:text-slate-400"
        />
      </div>
      <Button 
        type="submit" 
        disabled={disabled || !value.trim()}
        className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl px-4"
      >
        <Send className="h-4 w-4" />
      </Button>
    </form>
  );
}
;