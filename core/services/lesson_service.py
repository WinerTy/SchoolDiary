from typing import TYPE_CHECKING, Union, List

from fastapi import HTTPException

from core.database import Lesson, User
from core.database.crud import ScheduleRepository
from core.database.crud import SchoolRepository
from core.database.schemas.lesson import CreateLesson, ReadLesson
from core.services.base_services import BaseService

if TYPE_CHECKING:
    from core.database.crud.school_subject import SchoolSubjectRepository
    from core.database.crud.lesson import LessonRepository


class LessonService(BaseService[Lesson, CreateLesson, ReadLesson, ReadLesson]):
    def __init__(
        self,
        lesson_repo: "LessonRepository",
        subject_repo: "SchoolSubjectRepository",
        school_repo: "SchoolRepository",
        schedule_repo: "ScheduleRepository",
    ):
        super().__init__(
            repositories={
                "lesson": lesson_repo,
                "subject": subject_repo,
                "school": school_repo,
                "schedule": schedule_repo,
            }
        )

    async def create_lessons(
        self,
        school_id: int,
        create_data: Union[CreateLesson, List[CreateLesson]],
        user: User,
    ):
        school_repo: SchoolRepository = self.get_repo("school")
        school = await school_repo.get_school(
            school_id, validate_ownership=True, user=user
        )

        lesson_repo: LessonRepository = self.get_repo("lesson")
        if isinstance(create_data, list):
            await self._validate_lessons(create_data)
            return await lesson_repo.multiple_create(create_data)
        else:
            await self._validate_lessons(create_data)
            return await lesson_repo.create(create_data)

    async def _validate_lessons(
        self, lessons: Union[CreateLesson, List[CreateLesson]]
    ) -> None:
        """Валидация уроков перед созданием.

        Проверяет:
        - Существование расписания
        - Существование всех учебных предметов

        Args:
            lessons: Один урок или список уроков для валидации

        Raises:
            HTTPException: Если какие-то проверки не пройдены
        """
        if not lessons:
            return

        lesson_list = [lessons] if isinstance(lessons, CreateLesson) else lessons
        if not lesson_list:
            return

        # Получаем репозитории
        schedule_repo: ScheduleRepository = self.get_repo("schedule")
        subject_repo: SchoolSubjectRepository = self.get_repo("subject")

        # Проверяем расписание (один раз для всех уроков)
        schedule_id = lesson_list[0].schedule_id
        schedule = await schedule_repo.get_by_id(
            schedule_id,
            raise_ex=True,
            error_message=f"Schedule with id {schedule_id} not found",
        )

        # Собираем все subject_ids и проверяем за один запрос
        subject_ids = {lesson.school_subject_id for lesson in lesson_list}
        existing_ids = await subject_repo.get_by_ids(subject_ids)

        if missing_ids := subject_ids - existing_ids:
            raise HTTPException(
                status_code=404, detail=f"Subjects with ids {missing_ids} not found"
            )

        is_valid, lesson = schedule.validate_lessons(new_lessons=lesson_list)
        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"Conflict with lesson {lesson.school_subject_id} at {lesson.end_time}",
            )

    async def get_lesson(self, lesson_id: int) -> Lesson:
        """
        Получение урока по id.

        Args:
            lesson_id: id урока

        Returns:
            Урок

        Raises:
            HTTPException: 404 Если урок не найден
        """
        lesson_repo: LessonRepository = self.get_repo("lesson")
        return await lesson_repo.get_by_id(lesson_id)
