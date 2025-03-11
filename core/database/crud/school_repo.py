from typing import TYPE_CHECKING

from fastapi import HTTPException

from core.database import School
from core.database.crud.base.repository import BaseRepository
from core.database.schemas.school import CreateSchool, ReadSchool, UpdateSchool

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SchoolRepository(BaseRepository[School, CreateSchool, ReadSchool, UpdateSchool]):
    def __init__(self, db: "AsyncSession"):
        super().__init__(School, db)

    async def get_school_teachers(self, school_id: int) -> ReadSchool:
        school = await self.get_by_id(school_id)

        if school:
            await self.db.refresh(school, attribute_names=["teachers"])
            return school

    async def create_school(self, data: CreateSchool, director_id: int):
        school = await self.get_by_id(director_id)
        if school:
            raise HTTPException(status_code=400, detail="School already exists")

        created_school = self.create(data, director_id=director_id)
        return created_school

    async def add_teacher_to_school(self, school_id: int):
        pass
