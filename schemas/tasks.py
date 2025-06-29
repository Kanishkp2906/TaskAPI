from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import Optional

class Priority(str, Enum):
    low = 'LOW'
    medium = 'MEDIUM'
    high = 'HIGH'

class Status(str, Enum):
    done = 'DONE'
    pending = 'PENDING'

class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, description='title of the task')
    description: str = Field(..., min_length=3, description='description of the task')
    status: Status = Status.pending
    priority: Priority = Priority.low

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3)
    description: Optional[str] = Field(None, min_length=3)
    status: Optional[Status] = Status.pending
    priority: Optional[Priority] = Priority.low