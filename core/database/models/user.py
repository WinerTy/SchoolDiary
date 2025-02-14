from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.mixins.id_mixin import PkIntMixin
from core.database.models.choices import ChoicesRole
from .base import BaseModel
from .. import School

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(BaseModel, PkIntMixin, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(128), nullable=True)
    last_name: Mapped[str] = mapped_column(String(128), nullable=False)

    role: Mapped[str] = mapped_column(
        Enum(ChoicesRole),
        nullable=False,
        default=ChoicesRole.student,
        server_default=ChoicesRole.student.value,
    )

    school_id: Mapped[int] = mapped_column(
        ForeignKey("school.id", ondelete="CASCADE"), nullable=True
    )
    school: Mapped["School"] = relationship(
        "School", back_populates="teachers", foreign_keys=[school_id]
    )

    classroom_id: Mapped[int] = mapped_column(
        ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=True
    )
    classroom: Mapped["Classroom"] = relationship(
        "Classroom", back_populates="students", foreign_keys=[classroom_id]
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)

    def __str__(self):
        return self.full_name
