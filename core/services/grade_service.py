from fastapi import HTTPException

from core.database import Grade, Lesson
from core.database.crud import LessonRepository
from core.database.crud import UserRepository
from core.database.crud.grade import GradeRepository
from core.database.crud.grade.schemas import GradeCreate, GradeRead
from core.services.base_services import BaseService


class GradeService(BaseService[Grade, GradeCreate, GradeRead, GradeCreate]):
    def __init__(
        self,
        grade_repo: "GradeRepository",
        lesson_repo: "LessonRepository",
        user_repo: "UserRepository",
    ):
        super().__init__(
            repositories={"grade": grade_repo, "lesson": lesson_repo, "user": user_repo}
        )

    async def _validate_new_grade(self, create_data: GradeCreate) -> None:
        """
        Метод для валидации данных перед созданием оценки.
        """
        lesson_repo: LessonRepository = self.get_repo("lesson")
        user_repo: UserRepository = self.get_repo("user")

        user = await user_repo.get_by_id(
            create_data.user_id, error_message="User not found"
        )
        lesson: "Lesson" = await lesson_repo.get_by_id(
            create_data.lesson_id, error_message="Lesson not found"
        )
        in_class = lesson.check_user_in_class(user)

        if not in_class:
            raise HTTPException(
                status_code=400,
                detail="User is not in classroom of this lesson",
            )

    async def create_grade(self, grade_data: GradeCreate) -> Grade:
        """
        Метод для создания оценки.
        """
        await self._validate_new_grade(grade_data)
        grade_repo: GradeRepository = self.get_repo("grade")
        grade = await grade_repo.create(grade_data)
        return grade
