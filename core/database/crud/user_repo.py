from typing import TYPE_CHECKING

from sqlalchemy import select

from core.database import User
from core.database.schemas.user import UserCreate, UserRead
from .base_repo import BaseRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository[User, UserCreate, UserRead, UserRead]):
    def __init__(self, db: "AsyncSession"):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()
