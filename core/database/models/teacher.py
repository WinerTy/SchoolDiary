from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import BaseModel
from ..mixins import PkIntMixin

if TYPE_CHECKING:
    from .user import User


class Teacher(BaseModel, PkIntMixin):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"), nullable=False, unique=True
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="cascade")
    )

    subject: Mapped["Subject"] = relationship("Subject", foreign_keys=[subject_id])

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])

    def __str__(self):
        return self.user.full_name
