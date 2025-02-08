from typing import TYPE_CHECKING

from core.database import User
from core.database.schemas.user import UserCreate, UserRead
from .base_repo import BaseRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository[User, UserCreate, UserRead, UserRead]):
    def __init__(self, db: "AsyncSession"):
        super().__init__(User, db)
