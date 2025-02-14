from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, Depends

from api.dependencies.repository import get_school_repository
from api.v1.auth.fastapi_users import current_active_user
from core.database.schemas.school import CreateSchool, ReadSchool

if TYPE_CHECKING:
    from core.database.crud.school_repo import SchoolRepository
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


@router.get("/{school_id}/teachers/", response_model=ReadSchool)
async def get_school_teachers(
    school_id: int,
    repo: Annotated["SchoolRepository", Depends(get_school_repository)],
):
    result = await repo.get_school_teachers(school_id)
    return result
