'use client';

import { useState, useEffect, useRef } from 'react';
import { useAuthContext } from '@/components/auth/auth-provider';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { ConversationHistory } from './ConversationHistory';
import { useToast } from '@/hooks/use-toast';
import { ChatMessage, ChatConversation } from '@/types';
import { 
  getUserConversations, 
  getConversationDetail, 
  sendChatMessage 
} from '@/lib/api-client';
import { Bot, Plus, LayoutPanelLeft, Sparkles } from 'lucide-react';

export const ChatInterface = () => {
  const { user } = useAuthContext();
  const { toast } = useToast();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversations, setConversations] = useState<ChatConversation[]>([]);
  const [activeConversation, setActiveConversation] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load conversations when component mounts
  useEffect(() => {
    if (user?.id) {
      loadConversations();
    }
  }, [user]);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadConversations = async () => {
    try {
      if (!user?.id) return;
      const data = await getUserConversations(user.id);

      setConversations(data.conversations.map((conv: any) => ({
        id: conv.id,
        title: conv.title || 'New Conversation',
        createdAt: new Date(conv.created_at || conv.created_at),
        updatedAt: new Date(conv.updated_at || conv.updated_at)
      })));
    } catch (error) {
      console.error('Error loading conversations:', error);
      toast({
        title: 'Error',
        description: 'Failed to load conversation history',
        variant: 'destructive'
      });
    }
  };

  const loadConversation = async (conversationId: string) => {
    try {
      if (!user?.id) return;
      setIsLoading(true);
      const data = await getConversationDetail(user.id, conversationId);

      const conversationMessages = data.messages.map((msg: any) => ({
        id: msg.id,
        role: msg.role,
        content: msg.content,
        timestamp: new Date(msg.timestamp || msg.created_at)
      }));

      setMessages(conversationMessages);
      setActiveConversation(conversationId);
    } catch (error) {
      console.error('Error loading conversation:', error);
      toast({
        title: 'Error',
        description: 'Failed to load conversation history',
        variant: 'destructive'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const createNewConversation = () => {
    setMessages([]);
    setActiveConversation(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      id: `u-${Date.now()}`,
      role: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      if (!user?.id) return;
      const data = await sendChatMessage(user.id, inputValue, activeConversation || undefined);

      // Add assistant response to messages
      const assistantMessage: ChatMessage = {
        id: `a-${Date.now()}`,
        role: 'assistant',
        content: data.response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);

      if (!activeConversation) {
        setActiveConversation(data.conversation_id);
        loadConversations();
      }
    } catch (error) {
      console.error('Error sending message:', error);
      toast({
        title: 'Connection Error',
        description: 'AI service is currently unresponsive. Please check your network.',
        variant: 'destructive'
      });
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white">
      <div className="flex-1 flex flex-col min-w-0 border border-slate-200 rounded-xl overflow-hidden shadow-sm">
        {/* Header */}
        <header className="px-6 py-4 border-b border-slate-100 bg-slate-50 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 rounded-lg bg-indigo-600 flex items-center justify-center">
              <Bot className="h-5 w-5 text-white" />
            </div>
            <div>
              <h3 className="font-bold text-sm text-slate-900 leading-tight">AI Assistant</h3>
              <div className="flex items-center gap-1.5">
                <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Online</span>
              </div>
            </div>
          </div>
          
          <Button 
            onClick={createNewConversation} 
            variant="ghost" 
            size="sm"
            className="text-[10px] font-bold uppercase tracking-wider text-slate-500 hover:text-indigo-600 group"
          >
            <Plus className="h-3 w-3 mr-1 group-hover:scale-110 transition-transform" />
            New Chat
          </Button>
        </header>
        
        <ScrollArea className="flex-1 bg-white">
          <div className="max-w-4xl mx-auto w-full">
            <MessageList 
              messages={messages} 
              isLoading={isLoading} 
              userInitial={user?.name?.charAt(0).toUpperCase() || 'U'}
            />
            <div ref={messagesEndRef} className="h-4" />
          </div>
        </ScrollArea>
        
        {/* Input Area */}
        <div className="p-4 border-t border-slate-100 bg-slate-50">
          <div className="max-w-3xl mx-auto w-full">
            <MessageInput
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onSubmit={handleSubmit}
              disabled={isLoading}
            />
            <p className="text-[10px] text-center text-slate-400 mt-3 font-medium uppercase tracking-tight">
              AI uses MCP tools to manage your tasks naturally
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
;