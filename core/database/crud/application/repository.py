from typing import TYPE_CHECKING, Optional

from sqlalchemy import select

from core.database.models.choices import ChoicesApplicationStatus

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

from core.database.crud.base.repository import BaseRepository
from core.database import Applications
from core.database.schemas.application import (
    CreateApplication,
    ReadApplication,
    UpdateApplication,
)

from .validator import ApplicationValidator


class ApplicationRepository(
    BaseRepository[Applications, CreateApplication, ReadApplication, UpdateApplication]
):
    def __init__(self, db: "AsyncSession", validator: ApplicationValidator):
        super().__init__(Applications, db)
        self.validator = validator

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

    async def update(
        self, item_id: int, update_data: UpdateApplication, user_id: int
    ) -> Applications:
        instance = await self.get_by_id(item_id)
        self.validator.validate(instance=instance, user_id=user_id)
        return await super().update(item_id, update_data)
