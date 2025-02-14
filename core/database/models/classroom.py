from typing import List

from sqlalchemy import ForeignKey, String
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

    school: Mapped["School"] = relationship(
        "School", back_populates="classrooms", foreign_keys=[school_id]
    )
    class_teacher: Mapped["User"] = relationship(
        "User", foreign_keys=[class_teacher_id]
    )
    students: Mapped[List["User"]] = relationship(
        "User", back_populates="classroom", foreign_keys="[User.classroom_id]"
    )

    def __str__(self):
        return self.class_name
