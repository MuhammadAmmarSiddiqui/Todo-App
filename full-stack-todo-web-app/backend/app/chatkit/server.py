"""
ChatKit Server implementation that integrates with Gemini backend.
This bridges OpenAI ChatKit UI with our custom Gemini-based assistant.
"""

from chatkit.server import ChatKitServer
from chatkit.types import ThreadMetadata, UserMessageItem, ThreadStreamEvent
from typing import AsyncIterator, Any, Optional
from services.openai_assistant import assistant_service


class GeminiChatKitServer(ChatKitServer):
    """
    Custom ChatKit server that uses Gemini for AI responses.
    This allows ChatKit UI to work with our Gemini backend.
    """
    
    async def respond(
        self, 
        thread: ThreadMetadata, 
        input_user_message: Optional[UserMessageItem],
        context: Any
    ) -> AsyncIterator[ThreadStreamEvent]:
        """
        Handle incoming chat messages and stream responses.
        
        Args:
            thread: Thread metadata containing thread ID
            input_user_message: The user's message item
            context: Custom context (can contain user info, auth, etc)
            
        Yields:
            ThreadStreamEvent instances to stream back to the client
        """
        try:
            if not input_user_message:
                return
                
            # Extract message content
            user_message = ""
            if hasattr(input_user_message, 'content'):
                # Handle different content types
                content = input_user_message.content
                if isinstance(content, str):
                    user_message = content
                elif isinstance(content, list):
                    # Extract text from content array
                    for item in content:
                        if hasattr(item, 'text'):
                            user_message += item.text
            
            # Extract user ID from context or use default
            user_id = getattr(context, 'user_id', 1) if context else 1
            thread_id = str(thread.id) if hasattr(thread, 'id') else None
            
            # Call our Gemini assistant service
            result = await assistant_service.process_chat_message(
                user_message=user_message,
                user_id=user_id,
                conversation_id=thread_id
            )
            
            # Return text response
            # Note: Actual streaming would require yielding ThreadStreamEvent instances
            # For now, we'll work with the basic response
            if result['status'] == 'success':
                # In a real implementation, you'd yield proper ThreadStreamEvent objects
                # This is a simplified version
                yield result['response']
            
        except Exception as e:
            print(f"Error in ChatKit server respond: {e}")
            import traceback
            traceback.print_exc()
