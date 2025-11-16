from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.user import UserResponse
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    category_id: Optional[int] = None


class TaskResponse(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    owner: Optional[UserResponse] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=250)
    completed: Optional[bool] = None
    category_id: Optional[int] = None
