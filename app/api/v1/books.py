from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_permissions
from app.core.permissions import Permission
from app.models import User
from app.schemas.book import BookCreate, BookOut, BookUpdate
from app.services import book_service

router = APIRouter(tags=["books"])


@router.get(
    "/",
    response_model=List[BookOut],
    dependencies=[Depends(require_permissions([Permission.BOOK_READ]))],
)
async def list_books(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await book_service.list_books(db, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=BookOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions([Permission.BOOK_CREATE]))],
)
async def create_book(
    payload: BookCreate,
    db: AsyncSession = Depends(get_db),
):
    return await book_service.create_book(db, payload)


@router.patch(
    "/{book_id}",
    response_model=BookOut,
    dependencies=[Depends(require_permissions([Permission.BOOK_UPDATE]))],
)
async def update_book(
    book_id: int,
    payload: BookUpdate,
    db: AsyncSession = Depends(get_db),
):
    book = await book_service.update_book(db, book_id, payload)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return book


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permissions([Permission.BOOK_DELETE]))],
)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
):
    deleted = await book_service.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
