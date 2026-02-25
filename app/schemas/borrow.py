from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BorrowCreate(BaseModel):
    book_id: int
    user_id: Optional[int] = None  # defaults to current user if omitted
    days: int = 14
    notes: Optional[str] = None


class BorrowOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    status: str
    borrowed_at: datetime
    due_date: datetime
    returned_at: Optional[datetime] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

