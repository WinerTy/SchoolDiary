from enum import Enum

from sqlalchemy import Enum as SqlEnum, ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from core.database import BaseModel


class ChoicesStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"


class Friendship(BaseModel):
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    friend_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        SqlEnum(ChoicesStatus),
        nullable=False,
        default=ChoicesStatus.PENDING,
        server_default=ChoicesStatus.PENDING.value,
    )
