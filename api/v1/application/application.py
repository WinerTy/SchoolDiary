from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, Depends

from api.dependencies.repository import get_application_repository
from api.dependencies.services.get_service import get_application_service
from api.v1.auth.fastapi_users import current_active_user
from core.database import User
from core.database.schemas.application import (
    CreateApplication,
    ReadApplication,
    UpdateApplication,
)

if TYPE_CHECKING:
    from core.database.crud.application import ApplicationRepository
    from core.services.application_service import ApplicationService


router = APIRouter(
    prefix="/application",
    tags=["Application"],
)


@router.post("/create/", response_model=ReadApplication, status_code=201, description="Создание заявки на создание школы")
async def create_application(
    create_data: CreateApplication,
    user: Annotated[User, Depends(current_active_user)],
    service: Annotated["ApplicationService", Depends(get_application_service)],
):
    return await service.create(create_data, user_id=user.id)


@router.patch("/{application_id}")
async def update_application(
    application_id: int,
    update_data: UpdateApplication,
    user: Annotated["User", Depends(current_active_user)],
    repo: Annotated["ApplicationRepository", Depends(get_application_repository)],
):
    return await repo.update(application_id, update_data, user.id)
