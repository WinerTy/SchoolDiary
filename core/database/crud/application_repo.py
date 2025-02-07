from typing import TYPE_CHECKING, Optional

from sqlalchemy import select

from ..models.choices import ChoicesApplicationStatus

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

    async def get_one_by_status(
        self, status: ChoicesApplicationStatus
    ) -> Optional[Applications]:
        result = await self.db.execute(
            select(self.model).where(self.model.status == status)
        )
        record = result.scalars().first()
        record.status = ChoicesApplicationStatus.approved
        self.db.add(record)
        await self.db.commit()
        return record
