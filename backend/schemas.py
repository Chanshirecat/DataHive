from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# Shared base schema
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "Pending"
    priority: Optional[str] = "Medium"
    due_date: Optional[datetime] = None


# Schema for creating a task
class TaskCreate(TaskBase):
    pass


# Schema for updating a task
class TaskUpdate(TaskBase):
    pass


# Schema for returning a task from the database
class Task(TaskBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
