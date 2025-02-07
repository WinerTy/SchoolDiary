from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import mapped_column, Mapped


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now(), nullable=False
    )
