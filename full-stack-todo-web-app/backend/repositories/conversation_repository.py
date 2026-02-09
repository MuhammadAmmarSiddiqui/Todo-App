from typing import List, Optional
from sqlmodel import Session, select, desc
from uuid import UUID
from app.models.conversation import Conversation, ConversationCreate
from app.models.message import Message, MessageCreate


class ConversationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_conversation(self, conversation: ConversationCreate) -> Conversation:
        """Create a new conversation"""
        db_conversation = Conversation.model_validate(conversation)
        self.session.add(db_conversation)
        self.session.commit()
        self.session.refresh(db_conversation)
        return db_conversation

    def get_conversation_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        """Get a conversation by its ID"""
        return self.session.get(Conversation, conversation_id)

    def get_conversations_by_user(self, user_id: int, limit: int = 10, offset: int = 0) -> List[Conversation]:
        """Get conversations for a specific user"""
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(desc(Conversation.updated_at))
            .offset(offset)
            .limit(limit)
        )
        return self.session.exec(statement).all()

    def update_conversation(self, conversation_id: UUID, title: str) -> Optional[Conversation]:
        """Update a conversation's title"""
        db_conversation = self.session.get(Conversation, conversation_id)
        if db_conversation:
            db_conversation.title = title
            from datetime import datetime
            db_conversation.updated_at = datetime.utcnow()
            self.session.add(db_conversation)
            self.session.commit()
            self.session.refresh(db_conversation)
        return db_conversation

    def delete_conversation(self, conversation_id: UUID) -> bool:
        """Delete a conversation"""
        db_conversation = self.session.get(Conversation, conversation_id)
        if db_conversation:
            self.session.delete(db_conversation)
            self.session.commit()
            return True
        return False


class MessageRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_message(self, message: MessageCreate) -> Message:
        """Create a new message"""
        db_message = Message.model_validate(message)
        self.session.add(db_message)
        self.session.commit()
        self.session.refresh(db_message)
        return db_message

    def get_messages_by_conversation(self, conversation_id: UUID) -> List[Message]:
        """Get all messages for a specific conversation"""
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp)
        return self.session.exec(statement).all()

    def get_message_by_id(self, message_id: UUID) -> Optional[Message]:
        """Get a message by its ID"""
        return self.session.get(Message, message_id)

    def update_message(self, message_id: UUID, content: str) -> Optional[Message]:
        """Update a message's content"""
        db_message = self.session.get(Message, message_id)
        if db_message:
            db_message.content = content
            self.session.add(db_message)
            self.session.commit()
            self.session.refresh(db_message)
        return db_message

    def delete_message(self, message_id: UUID) -> bool:
        """Delete a message"""
        db_message = self.session.get(Message, message_id)
        if db_message:
            self.session.delete(db_message)
            self.session.commit()
            return True
        return False