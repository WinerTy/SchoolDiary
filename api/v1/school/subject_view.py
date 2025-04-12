from typing import Annotated, TYPE_CHECKING, Union, List

from fastapi import APIRouter, Depends

from api.dependencies.services.get_service import get_school_subject_service
from api.v1.auth.fastapi_users import (
    current_active_teacher_or_admin_in_school,
)
from core.database.crud.school_subject import (
    SchoolSubjectCreate,
    SchoolSubjectRead,
)

if TYPE_CHECKING:
    from core.services.school_subject_service import SchoolSubjectService

router: APIRouter = APIRouter(
    prefix="/subject",
    tags=["School", "Subject"],
)


@router.get("/{school_id}")
async def get_school_subjects(
    school_id: int,
    service: Annotated["SchoolSubjectService", Depends(get_school_subject_service)],
):
    result = await service.get_subjects(school_id)
    return result


@router.post(
    "/{school_id}/",
    response_model=Union[SchoolSubjectRead, List[SchoolSubjectRead]],
    dependencies=[Depends(current_active_teacher_or_admin_in_school)],
    description="Универсальное создание школьных предметов, поддерживает создание одного или нескольких предметов одновременно",
)
async def create_new_subject(
    create_data: Union[SchoolSubjectCreate, List[SchoolSubjectCreate]],
    service: Annotated["SchoolSubjectService", Depends(get_school_subject_service)],
):
    result = await service.create_subject_v2(create_data)
    return result
