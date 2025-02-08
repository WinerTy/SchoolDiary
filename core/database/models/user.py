from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.mixins.id_mixin import PkIntMixin
from core.database.models.choices import ChoicesRole
from .base import BaseModel
from .. import School

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(BaseModel, PkIntMixin, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"

    role: Mapped[str] = mapped_column(
        Enum(ChoicesRole),
        nullable=False,
        default=ChoicesRole.student,
        server_default=ChoicesRole.student.value,
    )
    school_id: Mapped[int] = mapped_column(
        ForeignKey("school.id", ondelete="CASCADE"), nullable=True
    )

    # Указываем явно, что связь с School осуществляется через school_id
    school: Mapped["School"] = relationship(
        "School", back_populates="teachers", foreign_keys=[school_id]
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
