from core.database import Lesson
from core.database.crud.base.repository import BaseRepository
from core.database.schemas.lesson import CreateLesson, ReadLesson
from core.services.base_services import BaseService


class LessonService(BaseService[Lesson, CreateLesson, ReadLesson, ReadLesson]):
    def __init__(
        self,
        lesson_repo: BaseRepository,
    ):
        super().__init__(repositories={"lesson": lesson_repo})
