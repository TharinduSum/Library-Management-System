import asyncio
import json

from sqlalchemy import select

from app.core.permissions import ROLE_PERMISSIONS, RoleName, permissions_to_strings
from app.core.security import hash_password
from app.db.session import AsyncSessionLocal, Base, engine
from app.models import Role, User  # ensure models are imported so metadata is populated


async def seed() -> None:
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # Seed roles
        for role_name, perms in ROLE_PERMISSIONS.items():
            existing = await db.execute(select(Role).where(Role.name == role_name.value))
            if not existing.scalar_one_or_none():
                role = Role(
                    name=role_name.value,
                    description=f"{role_name.value.capitalize()} role",
                    permissions=json.dumps(permissions_to_strings(perms)),
                )
                db.add(role)

        await db.flush()

        # Seed admin user
        admin_role_result = await db.execute(
            select(Role).where(Role.name == RoleName.ADMIN.value)
        )
        admin_role = admin_role_result.scalar_one()

        existing_admin = await db.execute(select(User).where(User.username == "admin"))
        if not existing_admin.scalar_one_or_none():
            admin = User(
                email="admin@library.com",
                username="admin",
                hashed_password=hash_password("Admin@1234"),
                full_name="System Administrator",
                role_id=admin_role.id,
            )
            db.add(admin)
            print("✅ Admin user created: admin / Admin@1234")
        else:
            print("ℹ️  Admin user already exists")

        await db.commit()
        print("✅ Seed completed")


if __name__ == "__main__":
    asyncio.run(seed())
