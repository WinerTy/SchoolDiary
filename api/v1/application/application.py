from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import Response

from api.dependencies.services.application_service import get_application_service
from api.v1.auth.fastapi_users import current_active_user
from core.database import User
from core.database.models.choices import ChoicesApplicationStatus
from core.database.schemas.application import CreateApplication, ReadApplication
from core.services.application_service import ApplicationService
from utils.smtp.email import send_test_email, EmailSchema

router = APIRouter(
    prefix="/application",
    tags=["Application"],
)


@router.post("/create/", response_model=ReadApplication, status_code=201)
async def create_application(
    create_data: CreateApplication,
    user: Annotated[User, Depends(current_active_user)],
    service: Annotated["ApplicationService", Depends(get_application_service)],
):
    return await service.create(create_data, user_id=user.id)


@router.get("/test/{status}")
async def test_event(
    status: ChoicesApplicationStatus,
    service: Annotated["ApplicationService", Depends(get_application_service)],
):
    return await service.repository.get_one_by_status(status)


@router.post("/smtp/")
async def send_email(email: EmailSchema):
    await send_test_email(email)
    return Response("OK")
