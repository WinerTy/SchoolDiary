from typing import Union, List, Annotated

from fastapi import APIRouter
from fastapi import Depends

from api.dependencies.services.get_service import get_lesson_service
from api.v1.auth.fastapi_users import current_active_teacher_user_or_admin_user
from core.database import User
from core.database.schemas.lesson import CreateLesson
from core.services import LessonService

router: APIRouter = APIRouter(
    prefix="/lesson",
    tags=["School", "Lesson"],
)


@router.post("/{school_id}/")
async def create_lessons(
    school_id: int,
    lesson_data: Union[CreateLesson, List[CreateLesson]],
    user: Annotated["User", Depends(current_active_teacher_user_or_admin_user)],
    service: Annotated["LessonService", Depends(get_lesson_service)],
):
    result = await service.create_lessons(school_id, lesson_data, user)
    return result
