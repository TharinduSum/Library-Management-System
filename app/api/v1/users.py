from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_active_user, get_db, require_permissions
from app.core.permissions import Permission
from app.models import User
from app.schemas.api_key import APIKeyCreate, APIKeyOut
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services import api_key_service, user_service

router = APIRouter(tags=["users"])


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    existing = await user_service.get_user_by_username(db, payload.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    return await user_service.create_user(db, payload)


@router.get("/me", response_model=UserOut)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
):
    return current_user


@router.get(
    "/",
    response_model=List[UserOut],
    dependencies=[Depends(require_permissions([Permission.MEMBER_READ]))],
)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await user_service.get_all_users(db, skip=skip, limit=limit)


@router.put(
    "/{user_id}",
    response_model=UserOut,
    dependencies=[Depends(require_permissions([Permission.MEMBER_UPDATE]))],
)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
):
    user = await user_service.update_user(db, user_id, payload)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permissions([Permission.MEMBER_DELETE]))],
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    deleted = await user_service.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.get("/me/api-keys", response_model=List[APIKeyOut])
async def list_my_api_keys(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    return await api_key_service.list_user_api_keys(db, current_user.id)


@router.post(
    "/me/api-keys", response_model=APIKeyOut, status_code=status.HTTP_201_CREATED
)
async def create_my_api_key(
    payload: APIKeyCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    api_key, raw_key = await api_key_service.create_api_key(
        db, current_user, payload.name
    )
    return api_key
