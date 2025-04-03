from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.database import BaseModel

if TYPE_CHECKING:
    from .classroom import Classroom
    from .school_subject import SchoolSubject


class ClassroomSubjects(BaseModel):
    __tablename__ = "classroom_subjects"

    classroom_id: Mapped[int] = mapped_column(
        ForeignKey("classrooms.id"), primary_key=True
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("school_subject.id"), primary_key=True
    )

    classroom: Mapped["Classroom"] = relationship(back_populates="subjects")

    subject: Mapped["SchoolSubject"] = relationship(back_populates="classrooms")
