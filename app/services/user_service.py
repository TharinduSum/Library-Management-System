from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import RoleName
from app.core.security import hash_password
from app.models import Role, User
from app.schemas.user import UserCreate, UserUpdate


async def get_default_member_role(db: AsyncSession) -> Role:
    result = await db.execute(select(Role).where(Role.name == RoleName.MEMBER.value))
    role = result.scalar_one_or_none()
    if not role:
        raise RuntimeError("Default member role not found. Have you run the seeder?")
    return role


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    role = await get_default_member_role(db)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        role_id=role.id,
    )
    db.add(db_user)
    await db.flush()
    await db.refresh(db_user)
    return db_user


async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    result = await db.execute(
        select(User).order_by(User.id).offset(skip).limit(limit)
    )
    return list(result.scalars().all())


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def update_user(
    db: AsyncSession,
    user_id: int,
    user_data: UserUpdate,
) -> Optional[User]:
    db_user = await get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        return None

    update_dict = user_data.model_dump(exclude_unset=True)

    password = update_dict.pop("password", None)
    if password is not None:
        db_user.hashed_password = hash_password(password)

    role_id = update_dict.pop("role_id", None)
    if role_id is not None:
        db_user.role_id = role_id

    for key, value in update_dict.items():
        setattr(db_user, key, value)

    await db.flush()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    db_user = await get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        return False
    await db.delete(db_user)
    return True
