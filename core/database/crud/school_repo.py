from typing import TYPE_CHECKING

from fastapi import HTTPException
from sqlalchemy import select

from core.database import School
from core.database.crud.base_repo import BaseRepository
from core.database.schemas.school import CreateSchool, ReadSchool

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SchoolRepository(BaseRepository[School, CreateSchool, ReadSchool, ReadSchool]):
    def __init__(self, db: "AsyncSession"):
        super().__init__(School, db)

    async def get_school_teachers(self, school_id: int) -> ReadSchool:
        stmt = select(School).where(School.id == school_id)
        result = await self.db.execute(stmt)
        school = result.scalars().first()
        if school:
            await self.db.refresh(school, attribute_names=["teachers"])
            return school
        return HTTPException(status_code=404, detail="School not found")

    async def add_teacher_to_school(self, school_id: int):
        pass
