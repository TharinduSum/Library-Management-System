import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_permissions
from app.core.permissions import Permission
from app.schemas.role import RoleCreate, RoleOut
from app.services import role_service

router = APIRouter(tags=["roles"])


@router.get(
    "/",
    response_model=List[RoleOut],
    dependencies=[Depends(require_permissions([Permission.ROLE_MANAGE]))],
)
async def list_roles(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await role_service.list_roles(db, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=RoleOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permissions([Permission.ROLE_MANAGE]))],
)
async def create_role(
    payload: RoleCreate,
    db: AsyncSession = Depends(get_db),
):
    permissions = json.dumps([])
    return await role_service.create_role(
        db, payload.name, payload.description, permissions
    )
