from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

from .base_repo import BaseRepository
from core.database import Applications
from core.database.schemas.application import CreateApplication, ReadApplication


class ApplicationRepository(
    BaseRepository[Applications, CreateApplication, ReadApplication, ReadApplication]
):
    def __init__(self, db: "AsyncSession"):
        super().__init__(Applications, db)
