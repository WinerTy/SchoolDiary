from datetime import date
from typing import List

from sqlalchemy import ForeignKey, String, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import BaseModel
from core.database.mixins import PkIntMixin


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

    def __str__(self):
        return f"{self.class_name} - {self.year_of_graduation}"
