from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from schemas.tasks import TaskResponse
from typing import List, Optional

class UserRole(str, Enum):
    admin = 'Admin'
    user = 'User'

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, description='name of the user')
    email: EmailStr = Field(..., description='email of the user')
    role: UserRole = UserRole.user

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description='password of the user')

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = UserRole.user
    password: Optional[str] = None

class UserTaskResponse(UserBase):
    id : int
    tasks: List[TaskResponse] = []

    class Config:
        from_attributes = True



