from typing import TYPE_CHECKING

from core.database import Classroom
from core.database.crud.base_repo import BaseRepository
from core.database.schemas.classroom import (
    ReadClassroom,
    CreateClassroom,
    UpdateClassroom,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class ClassroomRepository(
    BaseRepository[Classroom, CreateClassroom, ReadClassroom, UpdateClassroom]
):
    def __init__(self, db: "AsyncSession"):
        super().__init__(Classroom, db)
