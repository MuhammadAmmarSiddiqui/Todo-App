from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)

class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Pydantic schemas for API
class UserCreate(SQLModel):
    email: str
    password: str
    name: Optional[str] = None

class UserPublic(UserBase):
    id: int
    created_at: datetime
