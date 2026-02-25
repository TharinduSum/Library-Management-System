from typing import Optional

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    isbn: str
    title: str
    author: str
    publisher: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    total_copies: int = 1
    available_copies: int = 1
    published_year: Optional[int] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    isbn: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    total_copies: Optional[int] = None
    available_copies: Optional[int] = None
    published_year: Optional[int] = None


class BookOut(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

