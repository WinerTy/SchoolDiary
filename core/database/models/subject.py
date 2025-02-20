from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import BaseModel
from core.database.mixins import PkIntMixin

if TYPE_CHECKING:
    from .lesson import Lesson


class Subject(BaseModel, PkIntMixin):
    __tablename__ = "subjects"

    subject_name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    lessons: Mapped[List["Lesson"]] = relationship("Lesson", back_populates="subject")

    def __str__(self):
        return self.subject_name
