from pydantic import BaseModel, Field
from datetime import datetime

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class CategoryUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)