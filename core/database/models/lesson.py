from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Time, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import BaseModel
from core.database.mixins import PkIntMixin

if TYPE_CHECKING:
    from .user import User
    from .subject import Subject
    from .schedule import Schedule
    from .grade import Grade


class Lesson(BaseModel, PkIntMixin):
    __tablename__ = "lessons"
    schedule_id: Mapped[int] = mapped_column(
        ForeignKey("schedules.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="cascade"), nullable=False
    )
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"), nullable=False
    )
    start_time: Mapped[Time] = mapped_column(Time, nullable=False)
    end_time: Mapped[Time] = mapped_column(Time, nullable=False)
    additional_info: Mapped[str] = mapped_column(Text, nullable=True)

    subject: Mapped["Subject"] = relationship(
        "Subject", back_populates="lessons", lazy="joined"
    )
    teacher: Mapped["User"] = relationship(
        "User", back_populates="lessons", foreign_keys=[teacher_id]
    )
    schedule: Mapped["Schedule"] = relationship("Schedule", back_populates="lessons")
    grades: Mapped[List["Grade"]] = relationship("Grade", back_populates="lesson")

    def __str__(self):
        return self.subject.subject_name
