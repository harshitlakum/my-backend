from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    done: bool = False
    # Use timezone-aware UTC timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
