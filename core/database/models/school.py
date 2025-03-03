from typing import List

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.requests import Request

from core.database import BaseModel
from core.database.mixins import PkIntMixin


class School(BaseModel, PkIntMixin):
    director_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"), nullable=False
    )

    school_name: Mapped[str] = mapped_column(String(128), nullable=False)
    school_address: Mapped[str] = mapped_column(String(128), nullable=False)
    school_description: Mapped[str] = mapped_column(Text, nullable=False)
    school_type: Mapped[str] = mapped_column(String(128), nullable=True)
    school_phone: Mapped[str] = mapped_column(String(21), nullable=False)

    director: Mapped["User"] = relationship("User", foreign_keys=[director_id])

    teachers: Mapped[List["User"]] = relationship(
        "User", back_populates="school", foreign_keys="[User.school_id]"
    )
    classrooms: Mapped[List["Classroom"]] = relationship(
        "Classroom", back_populates="school", foreign_keys="[Classroom.school_id]"
    )

    def __str__(self):
        return self.school_name

    # Метод который используется для отображения связи в админке
    async def __admin_repr__(self, request: Request):
        return self.school_name

    # Метод который используется для создания выпадающего списка в админке для связи
    async def __admin_select2_repr__(self, request: Request) -> str:
        return f"{self.school_name} - {self.school_address}"
