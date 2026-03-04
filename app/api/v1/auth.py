from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.schemas.auth import LoginRequest, RefreshRequest, TokenPair
from app.services import auth_service

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=TokenPair, status_code=status.HTTP_200_OK)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    return await auth_service.login(db, payload)


@router.post("/token", response_model=TokenPair)
async def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    payload = LoginRequest(username=form_data.username, password=form_data.password)
    return await auth_service.login(db, payload)


@router.post("/refresh", response_model=TokenPair, status_code=status.HTTP_200_OK)
async def refresh(payload: RefreshRequest):
    return await auth_service.refresh(payload)
