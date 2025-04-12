from typing import TYPE_CHECKING, Union, List, Optional

from core.database import Lesson, User, School
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
    ):
        super().__init__(
            repositories={
                "lesson": lesson_repo,
                "subject": subject_repo,
                "school": school_repo,
            }
        )

    async def get_school(
        self,
        school_id: int,
        *,
        validate_ownership: bool = False,
        validate_teacher: bool = False,
        user: Optional[User] = None
    ) -> School:
        """
        Получает школу с дополнительными проверками прав доступа

        Args:
            school_id: ID школы
            validate_ownership: Проверять, что пользователь - директор школы
            validate_teacher: Проверять, что пользователь - учитель школы
            user: Пользователь для проверки прав

        Returns:
            School: Объект школы

        Raises:
            HTTPException: 404 если школа не найдена
            PermissionError: Если проверка прав не пройдена
        """
        school_repo: SchoolRepository = self.get_repo("school")
        school = await school_repo.get_school_or_404(school_id)

        if validate_ownership or validate_teacher:
            if not user:
                raise ValueError("User is required for permission validation")

            if validate_ownership:
                school_repo.validator.validate_ownership(school, user)

            if validate_teacher:
                school_repo.validator.validate_teacher(school, user)

        return school

    async def create_lessons(
        self,
        school_id: int,
        create_data: Union[CreateLesson, List[CreateLesson]],
        user: User,
    ):
        school = await self.get_school(school_id, validate_ownership=True, user=user)

        lesson_repo: LessonRepository = self.get_repo("lesson")
        if isinstance(create_data, list):
            return await lesson_repo.multiple_create(create_data)
        else:
            return await lesson_repo.create(create_data)
