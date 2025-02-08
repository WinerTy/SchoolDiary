from typing import List

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import BaseModel
from core.database.mixins import PkIntMixin


class School(BaseModel, PkIntMixin):
    director_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"), nullable=False
    )

    school_address: Mapped[str] = mapped_column(String(128), nullable=False)
    school_description: Mapped[str] = mapped_column(Text, nullable=False)
    school_type: Mapped[str] = mapped_column(String(128), nullable=True)
    school_phone: Mapped[str] = mapped_column(String(21), nullable=False)

    director: Mapped["User"] = relationship("User", foreign_keys=[director_id])

    teachers: Mapped[List["User"]] = relationship(
        "User", back_populates="school", foreign_keys="[User.school_id]"
    )
