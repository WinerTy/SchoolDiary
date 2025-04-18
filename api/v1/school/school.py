from datetime import date
from typing import Annotated, TYPE_CHECKING, Optional

from fastapi import APIRouter, Depends

from api.dependencies.repository import (
    get_school_repository,
    get_lesson_repository,
    get_classroom_repository,
)
from api.dependencies.services.get_service import get_school_service
from api.v1.auth.fastapi_users import current_active_teacher_or_admin_in_school
from api.v1.auth.fastapi_users import current_active_user
from core.database.crud import ClassroomRepository
from core.database.schemas import SuccessResponse
from core.database.schemas.lesson import MultiCreateLessons
from core.database.schemas.schedule import ReadSchedule
from core.database.schemas.school import CreateSchool
from core.services.school_service import SchoolService

if TYPE_CHECKING:
    from core.database.crud import SchoolRepository
    from core.database.crud import LessonRepository
    from core.database import User


router = APIRouter(
    prefix="/school",
    tags=["School"],
)


@router.post("/")
async def create_school(
    user: Annotated["User", Depends(current_active_user)],
    repo: Annotated["SchoolRepository", Depends(get_school_repository)],
    create_data: CreateSchool,
):
    instance = await repo.create_school(create_data, director_id=user.id)
    return instance


# @router.get("/{school_id}/teachers/", response_model=ReadSchool)
# async def get_school_teachers(
#     school_id: int,
#     repo: Annotated["SchoolRepository", Depends(get_school_repository)],
# ):
#     result = await repo.get_school_teachers(school_id)
#     return result


@router.post(
    "/lesson/",
    response_model=SuccessResponse,
    status_code=201,
    dependencies=[Depends(current_active_teacher_or_admin_in_school)],
)
async def create_lessons(
    lesson_data: MultiCreateLessons,
    repo: Annotated["LessonRepository", Depends(get_lesson_repository)],
):
    result = await repo.multiple_create(lesson_data.lessons)
    return SuccessResponse(
        detail="Lessons created successfully",
        status=201,
        count_records=len(result),
    )


@router.get(
    "/{school_id}/{classroom_id}/schedule/",
    response_model=ReadSchedule,
)
async def get_schedule(
    school_id: int,
    classroom_id: int,
    service: Annotated["SchoolService", Depends(get_school_service)],
    schedule_date: Optional[date] = date.today(),
):
    result = await service.get_schedule_for_class(
        school_id, classroom_id, schedule_date
    )
    return result


@router.get("/{school_id}/schedule/")
async def get_school_schedule(
    school_id: int,
    service: Annotated["SchoolService", Depends(get_school_service)],
    schedule_date: Optional[date] = date.today(),
):
    result = await service.get_schedule_for_school(school_id, schedule_date)
    return result


@router.get("/test/{classroom_id}")
async def get_test(
    classroom_id: int,
    repo: Annotated["ClassroomRepository", Depends(get_classroom_repository)],
):
    res = await repo.get_by_id(classroom_id)
    print(res.subjects)
    return res
