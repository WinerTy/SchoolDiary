from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from starlette.requests import Request

from core.database import BaseModel
from core.database.mixins import PkIntMixin

if TYPE_CHECKING:
    pass


class Subject(BaseModel, PkIntMixin):
    __tablename__ = "subjects"

    subject_name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(256), nullable=True)

    def __str__(self):
        return self.subject_name

    async def __admin_repr__(self, request: Request):
        return self.subject_name
