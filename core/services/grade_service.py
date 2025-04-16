from typing import TYPE_CHECKING

from fastapi import HTTPException

from core.database import Grade, Lesson, User
from core.database.crud import LessonRepository
from core.database.crud import UserRepository
from core.database.crud.grade import GradeRepository
from core.database.crud.grade.schemas import GradeCreate, GradeRead
from core.services.base_services import BaseService

if TYPE_CHECKING:
    from core.services import LessonService


class GradeService(BaseService[Grade, GradeCreate, GradeRead, GradeCreate]):
    def __init__(
        self,
        grade_repo: "GradeRepository",
        lesson_repo: "LessonRepository",
        user_repo: "UserRepository",
        lesson_service: "LessonService",
    ):
        super().__init__(
            repositories={
                "grade": grade_repo,
                "lesson": lesson_repo,
                "user": user_repo,
            },
            services={"lesson": lesson_service},
        )

    async def check_lesson_exists(self, lesson_id: int) -> Lesson:
        lesson_service: "LessonService" = self.get_service("lesson")
        return await lesson_service.get_lesson(lesson_id)

    async def _validate_new_grade(
        self, create_data: GradeCreate, teacher: "User"
    ) -> None:
        """
        Метод для валидации данных перед созданием оценки.

        Args:
            create_data: Данные для создания оценки
            teacher: Преподаватель(текущий пользователь)

        returns:
            None

        Raises:
            HTTPException: 400 Если ученик, которому ставят оценку не является учеником класса для текущего урока
            HTTPException: 403 Если пользователь не является преподователем текущего урока
            HTTPException: 404 Если урок не найден
        """
        user_repo: UserRepository = self.get_repo("user")
        user = await user_repo.get_by_id(
            create_data.user_id, error_message="User not found"
        )
        lesson: "Lesson" = await self.check_lesson_exists(create_data.lesson_id)

        if lesson.teacher != teacher:
            raise HTTPException(
                status_code=403, detail="We are not teacher for this lesson"
            )

        in_class = lesson.check_user_in_class(user)

        if not in_class:
            raise HTTPException(
                status_code=400,
                detail="User is not in classroom of this lesson",
            )

    async def create_grade(self, grade_data: GradeCreate, user: "User") -> Grade:
        """
        Метод для создания оценки.
        """
        await self._validate_new_grade(grade_data, teacher=user)
        grade_repo: GradeRepository = self.get_repo("grade")
        grade = await grade_repo.create(grade_data)
        return grade
