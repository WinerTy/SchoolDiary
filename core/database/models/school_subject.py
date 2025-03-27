from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import BaseModel
from core.database.mixins import PkIntMixin

if TYPE_CHECKING:
    from .school import School


class SchoolSubject(BaseModel, PkIntMixin):
    school_id: Mapped[int] = mapped_column(ForeignKey("school.id"), nullable=False)
    school: Mapped["School"] = relationship("School", back_populates="school_subject")

    subject_name: Mapped[str] = mapped_column(String(128), nullable=False)

    __table_args__ = (
        UniqueConstraint("school_id", "subject_name", name="unique_school_subject"),
    )

    def __str__(self) -> str:
        return self.subject_name
