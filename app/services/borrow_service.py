from datetime import datetime, timedelta, timezone
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import RoleName
from app.models import Book, Borrow, User
from app.schemas.borrow import BorrowCreate
from fastapi import HTTPException, status


async def borrow_book(
    db: AsyncSession,
    current_user: User,
    payload: BorrowCreate,
) -> Borrow:
    if current_user.role and current_user.role.name == RoleName.MEMBER.value:
        user_id = current_user.id
    else:
        user_id = payload.user_id or current_user.id

    book_result = await db.execute(select(Book).where(Book.id == payload.book_id))
    book = book_result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if book.available_copies <= 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="No copies available")

    now = datetime.now(timezone.utc)
    borrow = Borrow(
        user_id=user_id,
        book_id=payload.book_id,
        status="active",
        borrowed_at=now,
        due_date=now + timedelta(days=payload.days),
        notes=payload.notes,
    )
    book.available_copies -= 1
    db.add(borrow)
    await db.flush()
    await db.refresh(borrow)
    return borrow


async def list_borrows(
    db: AsyncSession,
    current_user: User,
    skip: int = 0,
    limit: int = 100,
) -> List[Borrow]:
    stmt = select(Borrow).order_by(Borrow.id).offset(skip).limit(limit)
    if current_user.role and current_user.role.name == RoleName.MEMBER.value:
        stmt = stmt.where(Borrow.user_id == current_user.id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_borrow(db: AsyncSession, borrow_id: int) -> Optional[Borrow]:
    result = await db.execute(select(Borrow).where(Borrow.id == borrow_id))
    return result.scalar_one_or_none()


async def return_borrow(
    db: AsyncSession,
    current_user: User,
    borrow_id: int,
) -> Borrow:
    borrow = await get_borrow(db, borrow_id)
    if not borrow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrow not found")

    if current_user.role and current_user.role.name == RoleName.MEMBER.value:
        if borrow.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    if borrow.returned_at is not None or borrow.status == "returned":
        return borrow

    book_result = await db.execute(select(Book).where(Book.id == borrow.book_id))
    book = book_result.scalar_one_or_none()
    if book:
        book.available_copies += 1

    borrow.status = "returned"
    borrow.returned_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(borrow)
    return borrow

