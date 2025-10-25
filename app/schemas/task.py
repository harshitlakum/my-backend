from datetime import datetime
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=120)

class TaskRead(BaseModel):
    id: int
    title: str
    done: bool
    created_at: datetime

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    done: bool | None = None
