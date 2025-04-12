from typing import TYPE_CHECKING

from fastapi import HTTPException

from core.database import School
from core.database.crud.base.repository import BaseRepository
from core.database.schemas.school import CreateSchool, ReadSchool, UpdateSchool
from .validator import SchoolValidator

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SchoolRepository(BaseRepository[School, CreateSchool, ReadSchool, UpdateSchool]):
    def __init__(self, db: "AsyncSession", validator: "SchoolValidator"):
        self.validator = validator
        super().__init__(School, db)

    async def get_school_teachers(self, school_id: int) -> ReadSchool:
        school = await self.get_by_id(school_id)
        return school

    async def create_school(self, data: CreateSchool, director_id: int):
        school = await self.get_with_filter(
            {"director_id": director_id}, raise_ex=False
        )
        if school:
            raise HTTPException(status_code=400, detail="School already exists")

        created_school = await self.create(data, director_id=director_id)
        return created_school

    async def add_teacher_to_school(self, school_id: int):
        pass

    async def get_school_or_404(self, school_id: int) -> School:
        school = await self.get_by_id(school_id)
        if not school:
            raise HTTPException(status_code=404, detail="School not found")
        return school
