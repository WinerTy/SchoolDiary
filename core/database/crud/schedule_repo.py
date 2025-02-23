from typing import TYPE_CHECKING

from core.database import Schedule
from core.database.crud.base_repo import BaseRepository
from core.database.schemas.schedule import CreateSchedule, ReadSchedule

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class ScheduleRepository(
    BaseRepository[Schedule, CreateSchedule, ReadSchedule, ReadSchedule]
):
    def __init__(self, db: "AsyncSession"):
        super().__init__(Schedule, db)
