from sqlmodel import SQLModel, Field, Column
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from enum import Enum
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import JSON


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"
    tool = "tool"


class MessageBase(SQLModel):
    conversation_id: UUID
    role: MessageRole
    content: str = Field(max_length=10000)
    tool_calls: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    tool_responses: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))


class Message(MessageBase, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Pydantic schemas for API
class MessageCreate(MessageBase):
    pass


class MessageUpdate(SQLModel):
    content: Optional[str] = None
    tool_calls: Optional[Dict[str, Any]] = None
    tool_responses: Optional[Dict[str, Any]] = None


class MessagePublic(MessageBase):
    id: UUID
    timestamp: datetime