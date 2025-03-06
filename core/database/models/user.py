from typing import TYPE_CHECKING, List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from jinja2 import Template
from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.requests import Request

from core.database.mixins.id_mixin import PkIntMixin
from core.database.models.choices import ChoicesRole
from .base import BaseModel

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from .teacher import Teacher
    from .school import School
    from .classroom import Classroom
    from .lesson import Lesson
    from .grade import Grade


class User(BaseModel, PkIntMixin, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(128), nullable=True)
    last_name: Mapped[str] = mapped_column(String(128), nullable=False)

    role: Mapped[str] = mapped_column(
        Enum(ChoicesRole),
        nullable=False,
        default=ChoicesRole.user,
        server_default=ChoicesRole.user.value,
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
    teacher_info: Mapped["Teacher"] = relationship(
        "Teacher", back_populates="user", uselist=False
    )
    lessons: Mapped[List["Lesson"]] = relationship("Lesson", back_populates="teacher")

    grades: Mapped[List["Grade"]] = relationship("Grade", back_populates="user")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)

    def __str__(self):
        return self.full_name

    async def __admin_repr__(self, request: Request) -> str:
        return self.full_name

    async def __admin_select2_repr__(self, request: Request) -> str:
        template = Template(
            """<span>{{ full_name }}</span>""",
            autoescape=True,
        )
        return template.render(full_name=self.full_name)
