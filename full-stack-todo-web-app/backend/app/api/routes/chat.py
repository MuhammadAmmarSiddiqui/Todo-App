from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional
from uuid import UUID
from app.database.session import get_session
from services.openai_assistant import assistant_service
from repositories.conversation_repository import ConversationRepository, MessageRepository
from app.models.conversation import ConversationCreate
from app.models.message import MessageCreate, MessageRole
from app.core.auth import verify_jwt_token


from pydantic import BaseModel



class ChatMessageRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None


router = APIRouter(prefix="/chat", tags=["chat"])





@router.post("/{user_id}/")
async def process_chat_message(
    user_id: int,
    request: ChatMessageRequest,
    token: dict = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    print(f"DEBUG: Endpoint /chat/{user_id}/ called with message: {request.message}")
    """
    Process natural language input and return AI response
    """
    # Verify the user ID matches the token
    if str(token.get("sub")) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized: Token does not match user ID"
        )
    
    # Get repositories
    conversation_repo = ConversationRepository(session)
    message_repo = MessageRepository(session)
    existing_conversation = None
    
    # If no conversation ID provided, create a new conversation
    if not request.conversation_id:
        conversation_data = ConversationCreate(user_id=user_id, title=request.message[:50] + "..." if len(request.message) > 50 else request.message)
        conversation = conversation_repo.create_conversation(conversation_data)
        conversation_id = conversation.id
    else:
        # Verify the conversation belongs to the user
        conversation_id = request.conversation_id
        existing_conversation = conversation_repo.get_conversation_by_id(conversation_id)
        if not existing_conversation or existing_conversation.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or does not belong to user"
            )
    
    # Create a message record for the user's input
    user_message = MessageCreate(
        conversation_id=conversation_id,
        role=MessageRole.user,
        content=request.message
    )
    message_repo.create_message(user_message)
    
    # Process the message with the AI assistant
    result = await assistant_service.process_chat_message(request.message, user_id, str(conversation_id))
    
    if result["status"] == "error":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Unknown error occurred")
        )
    
    # Create a message record for the assistant's response
    assistant_message = MessageCreate(
        conversation_id=conversation_id,
        role=MessageRole.assistant,
        content=result["response"]
    )
    message_repo.create_message(assistant_message)
    
    # Update the conversation's updated_at timestamp
    conv_title = existing_conversation.title if (request.conversation_id and existing_conversation) else request.message[:50]
    conversation_repo.update_conversation(conversation_id, conv_title)
    
    return {
        "response": result["response"],
        "conversation_id": result["conversation_id"],
        "tool_calls": []  # Placeholder - in a real implementation, this would come from the assistant
    }


@router.get("/{user_id}/conversations")
async def get_user_conversations(
    user_id: int,
    limit: int = 10,
    offset: int = 0,
    token: dict = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Retrieve user's conversation history
    """
    # Verify the user ID matches the token
    if str(token.get("sub")) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized: Token does not match user ID"
        )
    
    conversation_repo = ConversationRepository(session)
    conversations = conversation_repo.get_conversations_by_user(user_id, limit, offset)
    
    # Count total conversations for pagination
    # Note: In a real implementation, we'd have a separate method to get the count
    # For now, we'll just return the conversations we retrieved
    return {
        "conversations": conversations,
        "total": len(conversations)  # This is not the actual total, just the count of returned items
    }


@router.get("/{user_id}/conversation/{conversation_id}")
async def get_specific_conversation(
    user_id: int,
    conversation_id: UUID,
    token: dict = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Retrieve specific conversation
    """
    # Verify the user ID matches the token
    if str(token.get("sub")) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized: Token does not match user ID"
        )
    
    conversation_repo = ConversationRepository(session)
    message_repo = MessageRepository(session)
    
    # Verify the conversation belongs to the user
    conversation = conversation_repo.get_conversation_by_id(conversation_id)
    if not conversation or conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or does not belong to user"
        )
    
    # Get all messages for this conversation
    messages = message_repo.get_messages_by_conversation(conversation_id)
    
    return {
        "conversation": conversation,
        "messages": messages
    }


@router.delete("/{user_id}/conversation/{conversation_id}")
async def delete_conversation(
    user_id: int,
    conversation_id: UUID,
    token: dict = Depends(verify_jwt_token),
    session: Session = Depends(get_session)
):
    """
    Delete specific conversation
    """
    # Verify the user ID matches the token
    if str(token.get("sub")) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized: Token does not match user ID"
        )
    
    conversation_repo = ConversationRepository(session)
    
    # Verify the conversation belongs to the user
    conversation = conversation_repo.get_conversation_by_id(conversation_id)
    if not conversation or conversation.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or does not belong to user"
        )
    
    success = conversation_repo.delete_conversation(conversation_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete conversation"
        )
    
    return {"message": "Conversation deleted successfully"}