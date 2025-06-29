from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum as PyEnum

Base = declarative_base()

class UserRole(str, PyEnum):
    admin = 'Admin'
    user = 'User'

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    role = Column(Enum(UserRole), default = UserRole.user)
    tasks = relationship('Tasks', back_populates='user')

class Priority(str, PyEnum):
    low = 'LOW'
    medium = 'MEDIUM'
    high = "HIGH"

class TaskStatus(str, PyEnum):
    done = 'DONE'
    pending = 'PENDING'

class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, index=True)
    description = Column(String(255))
    status = Column(Enum(TaskStatus), default=TaskStatus.pending)
    priority = Column(Enum(Priority), default= Priority.low)
    created_at = Column(TIMESTAMP, default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', back_populates='tasks')

