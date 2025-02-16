from datetime import datetime

from sqlalchemy import ForeignKey, Enum, text, String
from sqlalchemy.orm import Mapped, mapped_column

from core.database.mixins import PkIntMixin, TimestampMixin
from .base import BaseModel
from .choices import ChoicesInviteStatus


class Invitation(BaseModel, PkIntMixin, TimestampMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"))
    token: Mapped[str] = mapped_column(String(36), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(
        server_default=text("(CURRENT_TIMESTAMP + INTERVAL '3 DAYS')")
    )
    status: Mapped[str] = mapped_column(
        Enum(ChoicesInviteStatus),
        nullable=False,
        default=ChoicesInviteStatus.pending,
        server_default=ChoicesInviteStatus.pending.value,
    )

    def __str__(self):
        return self.token
