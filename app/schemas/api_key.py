from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class APIKeyCreate(BaseModel):
    name: str


class APIKeyOut(BaseModel):
    id: int
    name: str
    is_active: bool
    created_at: datetime
    expires_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

