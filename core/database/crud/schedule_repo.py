from datetime import date, timedelta
from typing import TYPE_CHECKING, Optional, Tuple

from fastapi import HTTPException
from sqlalchemy import select, and_

from core.database import Schedule, Classroom
from core.database.crud.base_repo import BaseRepository
from core.database.schemas.schedule import CreateSchedule, ReadSchedule

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class ScheduleRepository(
    BaseRepository[Schedule, CreateSchedule, ReadSchedule, ReadSchedule]
):
    def __init__(self, db: "AsyncSession"):
        super().__init__(Schedule, db)

    @staticmethod
    async def _get_base_query():
        return select(Schedule).join(Classroom).where(Classroom.is_graduated == False)

    @staticmethod
    def get_week_dates(schedule_date: date) -> Tuple[date, date]:
        start_of_week = schedule_date - timedelta(days=schedule_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return start_of_week, end_of_week

    async def get_schedule_by_classroom_id(
            self, classroom_id: int, schedule_date: Optional[date] = None
    ) -> Schedule:
        if schedule_date is None:
            schedule_date = date.today()

        stmt = await self._get_base_query()
        stmt = stmt.where(
            and_(
                Classroom.id == classroom_id,
                Schedule.schedule_date == schedule_date,
            )
        )
        result = await self.db.execute(stmt)
        result = result.scalars().first()
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Schedule for classroom_id: {classroom_id}. As of date: {schedule_date} not found",
            )
        return result

    async def get_schedule_for_school(
            self, school_id: int, schedule_date: Optional[date] = date.today()
    ):
        start_week, end_week = self.get_week_dates(schedule_date)
        stmt = await self._get_base_query()
        stmt = stmt.where(
            and_(
                Classroom.school_id == school_id,
                Schedule.schedule_date >= start_week,
                Schedule.schedule_date <= end_week,
            )
        )

        result = await self.db.execute(stmt)
        return result.scalars().unique().all()
