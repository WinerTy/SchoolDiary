from typing import TYPE_CHECKING, List

from fastapi import Request
from jinja2 import Template
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import BaseModel
from core.database.mixins import PkIntMixin

if TYPE_CHECKING:
    from .school import School
    from .classroom_subjects import ClassroomSubjects
    from .lesson import Lesson

class SchoolSubject(BaseModel, PkIntMixin): 
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"), nullable=False)
    school: Mapped["School"] = relationship("School", back_populates="school_subject")

    subject_name: Mapped[str] = mapped_column(String(128), nullable=False)

    classrooms: Mapped[List["ClassroomSubjects"]] = relationship(
        back_populates="subject"
    )
    lessons: Mapped[List["Lesson"]] = relationship(
        "Lesson", back_populates="school_subjects"
    )
    __table_args__ = (
        UniqueConstraint("school_id", "subject_name", name="unique_school_subject"),
    )

    def __str__(self) -> str:
        return self.subject_name

    async def __admin_repr__(self, request: Request) -> str:
        return self.subject_name
    
    async def __admin_select2_repr__(self, request: Request) -> str:
        template = Template(
            """<span>Школа: {{ school_name }}, {{ subject_name }}</span>""",
            autoescape=True,
        )
        return template.render(subject_name=self.subject_name, school_name=self.school.school_name)
