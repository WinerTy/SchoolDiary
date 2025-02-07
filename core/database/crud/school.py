from typing import TYPE_CHECKING

from core.database import School
from core.database.crud.base_repo import BaseRepository
from core.database.schemas.school import CreateSchool, ReadSchool

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SchoolRepository(BaseRepository[School, CreateSchool, ReadSchool, ReadSchool]):
    def __init__(self, db: "AsyncSession"):
        super().__init__(School, db)
