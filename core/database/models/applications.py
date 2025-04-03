from sqlalchemy import String, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database.mixins import PkIntMixin, TimestampMixin
from .base import BaseModel
from .choices import ChoicesApplicationStatus


class Applications(BaseModel, PkIntMixin, TimestampMixin):
    director_full_name: Mapped[str] = mapped_column(String(128), nullable=False)
    director_phone: Mapped[str] = mapped_column(String(21), nullable=False)
    director_email: Mapped[str] = mapped_column(String(128), nullable=False)

    school_name: Mapped[str] = mapped_column(String(128), nullable=False)
    school_address: Mapped[str] = mapped_column(String(128), nullable=False)
    school_phone: Mapped[str] = mapped_column(String(21), nullable=False)
    school_description: Mapped[str] = mapped_column(Text, nullable=False)
    school_type: Mapped[str] = mapped_column(String(128), nullable=True)

    status: Mapped[str] = mapped_column(
        Enum(ChoicesApplicationStatus),
        nullable=False,
        default=ChoicesApplicationStatus.pending,
        server_default=ChoicesApplicationStatus.pending.value,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"), nullable=False
    )

    def __str__(self) -> str:
        return f"Заявка №{self.id}"
    
    
    @property
    def to_dict(self):
        return {
            "FIO": self.director_full_name,
            "school": self.school_name
        }