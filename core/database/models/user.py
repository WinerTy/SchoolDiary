from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from core.database.mixins.id_mixin import PkIntMixin
from core.database.models.base import BaseModel

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(BaseModel, PkIntMixin, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
