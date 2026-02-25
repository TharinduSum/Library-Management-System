from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class RoleSummary(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role_id: Optional[int] = None


class UserOut(UserBase):
    id: int
    is_active: bool
    role: Optional[RoleSummary] = None

    model_config = ConfigDict(from_attributes=True)

