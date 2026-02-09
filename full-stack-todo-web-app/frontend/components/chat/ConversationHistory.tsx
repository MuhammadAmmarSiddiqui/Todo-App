import { ChatConversation } from '@/types';
import { MessageSquare, Clock } from 'lucide-react';

interface ConversationHistoryProps {
  conversations: ChatConversation[];
  activeConversation: string | null;
  onSelectConversation: (id: string) => void;
}

export const ConversationHistory = ({ 
  conversations, 
  activeConversation, 
  onSelectConversation 
}: ConversationHistoryProps) => {
  return (
    <div className="space-y-1.5 animate-in fade-in duration-500">
      {conversations.length > 0 ? (
        conversations.map((conversation, i) => (
          <button
            key={conversation.id}
            className={`w-full text-left px-4 py-3 rounded-xl transition-all duration-200 group relative ${
              activeConversation === conversation.id
                ? 'bg-primary/10 text-primary border border-primary/20 shadow-sm'
                : 'hover:bg-accent/50 text-muted-foreground hover:text-foreground border border-transparent'
            }`}
            onClick={() => onSelectConversation(conversation.id)}
            style={{ animationDelay: `${i * 50}ms` }}
          >
            <div className="flex items-start gap-3">
              <MessageSquare className={`h-4 w-4 mt-0.5 shrink-0 transition-colors ${
                activeConversation === conversation.id ? 'text-primary' : 'text-muted-foreground/40 group-hover:text-primary/60'
              }`} />
              <div className="flex-1 min-w-0">
                <div className={`truncate text-sm font-semibold mb-0.5 tracking-tight ${
                  activeConversation === conversation.id ? 'text-primary' : ''
                }`}>
                  {conversation.title || 'Untitled Session'}
                </div>
                <div className="flex items-center gap-1.5 text-[10px] font-medium text-muted-foreground/50">
                  <Clock className="h-3 w-3" />
                  <span>{new Date(conversation.updatedAt).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}</span>
                </div>
              </div>
            </div>
            
            {activeConversation === conversation.id && (
               <div className="absolute right-2 top-1/2 -translate-y-1/2 w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
            )}
          </button>
        ))
      ) : (
        <div className="flex flex-col items-center justify-center py-10 px-4 text-center">
           <div className="h-12 w-12 rounded-full bg-muted/30 flex items-center justify-center mb-3">
              <MessageSquare className="h-5 w-5 text-muted-foreground/20" />
           </div>
           <p className="text-xs font-semibold text-muted-foreground/40 uppercase tracking-widest">
             No History
           </p>
        </div>
      )}
    </div>
  );
};