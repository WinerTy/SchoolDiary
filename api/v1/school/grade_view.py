from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies.services.get_service import get_grade_service
from api.v1.auth.fastapi_users import current_active_teacher_or_admin_in_school
from core.database.crud.grade.schemas import GradeCreate
from core.services import GradeService

router: APIRouter = APIRouter(
    prefix="/{school_id}/grade",
    tags=["School", "Grade"],
)


@router.post("/", dependencies=[Depends(current_active_teacher_or_admin_in_school)])
async def create_grade(
    grade_data: GradeCreate,
    service: Annotated["GradeService", Depends(get_grade_service)],
):
    result = await service.create_grade(grade_data)
    return result
