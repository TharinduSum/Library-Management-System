from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import generate_api_key
from app.models import APIKey, User


async def create_api_key(db: AsyncSession, user: User, name: str) -> tuple[APIKey, str]:
    raw_key, key_hash = generate_api_key()
    api_key = APIKey(name=name, key_hash=key_hash, user_id=user.id)
    db.add(api_key)
    await db.flush()
    await db.refresh(api_key)
    return api_key, raw_key


async def list_user_api_keys(db: AsyncSession, user_id: int) -> List[APIKey]:
    result = await db.execute(
        select(APIKey).where(APIKey.user_id == user_id).order_by(APIKey.id)
    )
    return list(result.scalars().all())
