from datetime import date
from typing import List, TYPE_CHECKING

from jinja2 import Template
from sqlalchemy import ForeignKey, String, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.requests import Request

from core.database import BaseModel
from core.database.mixins import PkIntMixin

if TYPE_CHECKING:
    from .school import School
    from .user import User
    from .schedule import Schedule
    from .classroom_subjects import ClassroomSubjects


class Classroom(BaseModel, PkIntMixin):
    __tablename__ = "classrooms"

    class_teacher_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"), nullable=False
    )
    class_name: Mapped[str] = mapped_column(String(16), nullable=False)

    school_id: Mapped[int] = mapped_column(
        ForeignKey("school.id", ondelete="cascade"), nullable=False
    )

    year_of_graduation: Mapped[date] = mapped_column(Date, nullable=False)

    is_graduated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    school: Mapped["School"] = relationship(
        "School", back_populates="classrooms", foreign_keys=[school_id]
    )
    class_teacher: Mapped["User"] = relationship(
        "User", foreign_keys=[class_teacher_id]
    )
    students: Mapped[List["User"]] = relationship(
        "User", back_populates="classroom", foreign_keys="[User.classroom_id]"
    )
    schedules: Mapped[List["Schedule"]] = relationship(
        "Schedule", back_populates="classroom", foreign_keys="[Schedule.classroom_id]"
    )

    subjects: Mapped[List["ClassroomSubjects"]] = relationship(
        back_populates="classroom",
        lazy="joined",
    )

    def __str__(self):
        return f"{self.class_name} - {self.year_of_graduation}"

    async def __admin_repr__(self, request: Request) -> str:
        return self.class_name

    async def __admin_select2_repr__(self, request: Request) -> str:
        template = Template("<span>{{ class_name }}</span>", autoescape=True)
        return template.render(class_name=self.class_name)
