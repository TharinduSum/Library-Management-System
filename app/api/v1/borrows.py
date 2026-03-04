from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, get_current_active_user, require_permissions
from app.core.permissions import Permission
from app.models import User
from app.schemas.borrow import BorrowCreate, BorrowOut
from app.services import borrow_service

router = APIRouter(tags=["borrows"])


@router.post(
    "/",
    response_model=BorrowOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions([Permission.BORROW_CREATE]))],
)
async def create_borrow(
    payload: BorrowCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    return await borrow_service.borrow_book(db, current_user, payload)


@router.get(
    "/",
    response_model=List[BorrowOut],
    dependencies=[Depends(require_permissions([Permission.BORROW_READ]))],
)
async def list_borrows(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    return await borrow_service.list_borrows(db, current_user, skip=skip, limit=limit)


@router.post(
    "/{borrow_id}/return",
    response_model=BorrowOut,
    dependencies=[Depends(require_permissions([Permission.BORROW_RETURN]))],
)
async def return_borrow(
    borrow_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    return await borrow_service.return_borrow(db, current_user, borrow_id)
