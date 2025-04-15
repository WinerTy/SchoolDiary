from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from core.database import BaseModel
from core.database.mixins import PkIntMixin

if TYPE_CHECKING:
    from .user import User
    from .lesson import Lesson


class Grade(PkIntMixin, BaseModel):
    __tablename__ = "grades"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), nullable=False)

    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    additional_info: Mapped[str] = mapped_column(String(256), nullable=True)

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
    lesson: Mapped["Lesson"] = relationship(
        "Lesson", foreign_keys=[lesson_id], lazy="joined"
    )

    @validates("grade")
    def validate_grade(self, key, value):
        if value < 1 or value > 5:
            raise ValueError("Grade must be between 1 and 5")
        return value

    def __str__(self):
        return f"{self.user.full_name} - {self.lesson.subject_name} - {self.grade}"
