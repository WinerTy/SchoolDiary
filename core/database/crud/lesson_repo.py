from typing import TYPE_CHECKING

from core.database import Lesson
from core.database.crud.base_repo import BaseRepository
from core.database.schemas.lesson import CreateLesson, ReadLesson, UpdateLesson

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class LessonRepository(BaseRepository[Lesson, CreateLesson, ReadLesson, UpdateLesson]):
    def __init__(self, db: "AsyncSession"):
        super().__init__(Lesson, db)
