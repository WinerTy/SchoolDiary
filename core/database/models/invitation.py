from datetime import datetime

from sqlalchemy import ForeignKey, Enum, text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.mixins import PkIntMixin, TimestampMixin
from .base import BaseModel
from .choices import ChoicesInviteStatus, ChoicesRole


class Invitation(BaseModel, PkIntMixin, TimestampMixin):
    invited_by: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"))
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
    invite_role: Mapped[str] = mapped_column(
        Enum(ChoicesRole),
        nullable=False,
        default=ChoicesRole.student,
        server_default=ChoicesRole.student.value,
    )

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id], lazy="joined")
    invited_by_user: Mapped["User"] = relationship("User", foreign_keys=[invited_by])

    def __str__(self):
        return self.token
