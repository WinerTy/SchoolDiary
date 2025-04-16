from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies.services.get_service import get_grade_service
from api.dependencies.validators.validator import check_school_exists
from api.v1.auth.fastapi_users import current_active_teacher_or_admin_in_school
from core.database import User
from core.database.crud.grade.schemas import GradeCreate, GradeRead
from core.services import GradeService
from schemas import NotFoundResponse, ForbiddenResponse

router: APIRouter = APIRouter(
    prefix="/{school_id}/grade",
    tags=["School", "Grade"],
    dependencies=[Depends(check_school_exists)],
    responses={
        404: {"model": NotFoundResponse, "description": "School not found"},
        403: {"model": ForbiddenResponse, "description": "Forbidden"},
    },
)


@router.post("/", response_model=GradeRead, status_code=201)
async def create_grade(
    grade_data: GradeCreate,
    user: Annotated["User", Depends(current_active_teacher_or_admin_in_school)],
    service: Annotated["GradeService", Depends(get_grade_service)],
):
    result = await service.create_grade(grade_data, user)
    return result
