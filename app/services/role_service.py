from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Role


async def list_roles(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Role]:
    result = await db.execute(select(Role).order_by(Role.id).offset(skip).limit(limit))
    return list(result.scalars().all())


async def get_role(db: AsyncSession, role_id: int) -> Role | None:
    result = await db.execute(select(Role).where(Role.id == role_id))
    return result.scalar_one_or_none()


async def create_role(
    db: AsyncSession, name: str, description: str | None = None, permissions: str = "[]"
) -> Role:
    role = Role(name=name, description=description, permissions=permissions)
    db.add(role)
    await db.flush()
    await db.refresh(role)
    return role
