from typing import TYPE_CHECKING

from sqlalchemy import select

from core.database import User
from core.database.crud.base.repository import BaseRepository
from core.database.models.choices import ChoicesRole
from .schemas import UserCreate, UserRead, UserUpdate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository[User, UserCreate, UserRead, UserUpdate]):
    def __init__(self, db: "AsyncSession"):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def change_user_role(self, user_id: int, role: ChoicesRole) -> User:
        update_data = UserUpdate(role=role)
        user = await super().update(user_id, update_data)
        return user
