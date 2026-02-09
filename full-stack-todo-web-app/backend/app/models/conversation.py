from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
import sqlalchemy.dialects.postgresql as pg


class ConversationBase(SQLModel):
    user_id: int = Field(gt=0)
    title: Optional[str] = Field(default=None, max_length=200)


class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Pydantic schemas for API
class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(SQLModel):
    title: Optional[str] = None


class ConversationPublic(ConversationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime