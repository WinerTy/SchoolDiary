from typing import TYPE_CHECKING

from sqlalchemy import select

from core.database import User
from core.database.schemas.user import UserCreate, UserRead
from .base_repo import BaseRepository
from ..models.choices import ChoicesRole

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository[User, UserCreate, UserRead, UserRead]):
    def __init__(self, db: "AsyncSession"):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def change_user_role(self, user_id: int, role: ChoicesRole) -> User | None:
        user = await self.get_by_id(user_id)
        user.role = role
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
