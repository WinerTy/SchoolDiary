from typing import TYPE_CHECKING

from core.database import Lesson
from core.database.crud.base.repository import BaseRepository
from core.database.schemas.lesson import CreateLesson, ReadLesson, UpdateLesson

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class LessonRepository(BaseRepository[Lesson, CreateLesson, ReadLesson, UpdateLesson]):
    def __init__(self, db: "AsyncSession"):
        super().__init__(Lesson, db)

    @staticmethod
    def _chck_time(lesson1: CreateLesson, lesson2: CreateLesson) -> bool:
        return (
            lesson1.start_time < lesson2.end_time
            and lesson1.end_time > lesson2.start_time
        )
