from typing import TYPE_CHECKING, List

from fastapi import Request
from jinja2 import Template
from sqlalchemy import ForeignKey, Time, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import BaseModel
from core.database.mixins import PkIntMixin

if TYPE_CHECKING:
    from .user import User
    from .schedule import Schedule
    from .grade import Grade
    from .school_subject import SchoolSubject


class Lesson(BaseModel, PkIntMixin):
    __tablename__ = "lessons"
    schedule_id: Mapped[int] = mapped_column(
        ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False
    )

    school_subject_id: Mapped[int] = mapped_column(
        ForeignKey("school_subject.id", ondelete="CASCADE"), nullable=False
    )
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"), nullable=False
    )
    start_time: Mapped[Time] = mapped_column(Time, nullable=False)
    end_time: Mapped[Time] = mapped_column(Time, nullable=False)
    additional_info: Mapped[str] = mapped_column(Text, nullable=True)

    school_subjects: Mapped["SchoolSubject"] = relationship(
        "SchoolSubject", back_populates="lessons", lazy="joined"
    )

    teacher: Mapped["User"] = relationship(
        "User", back_populates="lessons", foreign_keys=[teacher_id]
    )
    schedule: Mapped["Schedule"] = relationship(
        "Schedule", back_populates="lessons", lazy="joined"
    )
    grades: Mapped[List["Grade"]] = relationship("Grade", back_populates="lesson")

    def __str__(self):
        return self.school_subjects.subject_name

    def check_user_in_class(self, user: "User") -> bool:
        return user in self.schedule.classroom.students

    async def __admin_repr__(self, request: Request) -> str:
        return self.school_subjects.subject_name

    async def __admin_select2_repr__(self, request: Request) -> str:
        template = Template(
            """<span>{{ subject_name }}</span>""",
            autoescape=True,
        )
        return template.render(subject_name=self.school_subjects.subject_name)

    @property
    def subject_name(self) -> str:
        return self.school_subjects.subject_name
