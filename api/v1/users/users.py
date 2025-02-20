from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import Response

from api.dependencies.services.application_service import get_invitation_service
from api.v1.auth.fastapi_users import current_active_teacher_user_or_admin_user
from core.database.schemas.invite import CreateInvite

if TYPE_CHECKING:
    from core.services.invitation_service import InvitationService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(current_active_teacher_user_or_admin_user)],
)


@router.post("/invite/")
async def invite_user_for_group(
    invite_data: CreateInvite,
    service: Annotated["InvitationService", Depends(get_invitation_service)],
):
    await service.create_invite(user_id=invite_data.user_id)
    return Response(status_code=200, content="OK")


@router.get("/invite/accept/{token}")
async def accept_invite(
    token: str,
    service: Annotated["InvitationService", Depends(get_invitation_service)],
):
    result = await service.accept_invite(token=token)
    return result
