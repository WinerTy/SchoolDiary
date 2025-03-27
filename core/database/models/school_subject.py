from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import BaseModel
from core.database.mixins import PkIntMixin

if TYPE_CHECKING:
    from .school import School
    from .classroom_subjects import ClassroomSubjects


class SchoolSubject(BaseModel, PkIntMixin):
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"), nullable=False)
    school: Mapped["School"] = relationship("School", back_populates="school_subject")

    subject_name: Mapped[str] = mapped_column(String(128), nullable=False)

    classrooms: Mapped[List["ClassroomSubjects"]] = relationship(
        back_populates="subject"
    )

    __table_args__ = (
        UniqueConstraint("school_id", "subject_name", name="unique_school_subject"),
    )

    def __str__(self) -> str:
        return self.subject_name
