from datetime import date
from typing import TYPE_CHECKING, Optional

from fastapi import HTTPException
from sqlalchemy import select

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

    async def get_by_filter(self, school_id):
        pass

    async def get_schedule_by_classroom_id(
        self, classroom_id: int, schedule_date: Optional[date] = None
    ) -> Schedule:
        if schedule_date is None:
            schedule_date = date.today()

        stmt = select(Schedule).where(
            (Schedule.classroom_id == classroom_id)
            & (Schedule.schedule_date == schedule_date)
        )
        result = await self.db.execute(stmt)
        result = result.scalars().first()
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Schedule for classroom_id: {classroom_id}. As of date: {schedule_date} not found",
            )
        return result

    async def get_schedule_from_school(
        self, school_id, schedule_date: Optional[date] = None
    ):
        pass
