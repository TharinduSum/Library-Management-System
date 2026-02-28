from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Book
from app.schemas.book import BookCreate, BookUpdate


async def list_books(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Book]:
    result = await db.execute(select(Book).order_by(Book.id).offset(skip).limit(limit))
    return list(result.scalars().all())


async def create_book(db: AsyncSession, payload: BookCreate) -> Book:
    book = Book(**payload.model_dump())
    db.add(book)
    await db.flush()
    await db.refresh(book)
    return book


async def get_book(db: AsyncSession, book_id: int) -> Optional[Book]:
    result = await db.execute(select(Book).where(Book.id == book_id))
    return result.scalar_one_or_none()


async def update_book(
    db: AsyncSession,
    book_id: int,
    payload: BookUpdate,
) -> Optional[Book]:
    book = await get_book(db, book_id)
    if not book:
        return None
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(book, k, v)
    await db.flush()
    await db.refresh(book)
    return book


async def delete_book(db: AsyncSession, book_id: int) -> bool:
    book = await get_book(db, book_id)
    if not book:
        return False
    await db.delete(book)
    return True

