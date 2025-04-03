from datetime import date
from typing import Optional

from fastapi import HTTPException

from core.database import School
from core.database.crud.base.repository import BaseRepository
from core.database.schemas.school import CreateSchool, ReadSchool
from .base_services import BaseService


class SchoolService(BaseService[School, CreateSchool, ReadSchool, ReadSchool]):
    def __init__(
        self,
        school_repo: BaseRepository,
        lesson_repo: BaseRepository,
        schedule_repo: BaseRepository,
        classroom_repo: BaseRepository,
    ):
        super().__init__(
            repositories={
                "school": school_repo,
                "lesson": lesson_repo,
                "schedule": schedule_repo,
                "classroom": classroom_repo,
            }
        )

    async def _validate_param(self, school_id: int, classroom_id: int) -> bool:
        classroom_repo = self.get_repo("classroom")
        classroom = await classroom_repo.get_by_id(classroom_id)

        if classroom.school_id != school_id:
            raise HTTPException(
                detail="Класс не принадлежит данной школе или не существует",
                status_code=400,
            )

        return True

    async def get_schedule_for_class(
        self, school_id: int, classroom_id: int, schedule_date: Optional[date] = None
    ):
        is_verify = await self._validate_param(school_id, classroom_id)

        if is_verify:
            schedule_repo = self.get_repo("schedule")
            schedule = await schedule_repo.get_schedule_by_classroom_id(
                classroom_id, schedule_date
            )
            return schedule

    async def get_schedule_for_school(
        self, school_id: int, schedule_date: Optional[date] = date.today()
    ):
        schedule_repo = self.get_repo("schedule")
        schedule = await schedule_repo.get_schedule_for_school(school_id, schedule_date)
        return schedule
