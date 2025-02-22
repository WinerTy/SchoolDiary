from datetime import date
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import BaseModel
from core.database.mixins import PkIntMixin

if TYPE_CHECKING:
    from .classroom import Classroom
    from .lesson import Lesson


class Schedule(BaseModel, PkIntMixin):
    __tablename__ = "schedules"

    classroom_id: Mapped[int] = mapped_column(
        ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False
    )

    lessons: Mapped[List["Lesson"]] = relationship(
        "Lesson", back_populates="schedule", order_by="Lesson.start_time"
    )

    schedule_date: Mapped[date] = mapped_column(Date, nullable=False)

    classroom: Mapped["Classroom"] = relationship(
        "Classroom", back_populates="schedules"
    )

    def __str__(self) -> str:
        return f"{self.classroom} - {self.schedule_date}"
