from sqlmodel import SQLModel, Field, create_engine
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    user_id: int = Field(gt=0)


class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Pydantic schemas for API
class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskPublic(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

class TaskUpdateComplete(SQLModel):
    completed: bool