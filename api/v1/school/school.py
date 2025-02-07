from typing import Annotated

from fastapi import APIRouter, Depends

from api.dependencies.repo.school import get_school_repo
from api.v1.auth.fastapi_users import current_active_user
from core.database import User
from core.database.crud.school import SchoolRepository
from core.database.schemas.school import CreateSchool, ReadSchool

router = APIRouter(
    prefix="/school",
    tags=["School"],
)


@router.post("/", response_model=ReadSchool)
async def create_school(
    user: Annotated[User, Depends(current_active_user)],
    repo: Annotated[SchoolRepository, Depends(get_school_repo)],
    create_data: CreateSchool,
):
    record = await repo.create(create_data, director_id=user.id)
    return record
