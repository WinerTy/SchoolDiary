from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends

from api.dependencies.services.get_service import get_invitation_service
from api.v1.auth.fastapi_users import (
    current_active_teacher_user_or_admin_user,
    current_active_user,
)
from core.database.crud.invitation.schemas import (
    CreateInviteResponse,
    ReadInvite,
)
from core.database.schemas import SuccessResponse

if TYPE_CHECKING:
    from core.services.invitation_service import InvitationService
    from core.database import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/invite/", response_model=SuccessResponse)
async def invite_user_for_group(
    invite_data: CreateInviteResponse,
    user: Annotated["User", Depends(current_active_teacher_user_or_admin_user)],
    service: Annotated["InvitationService", Depends(get_invitation_service)],
):
    await service.create_invite(invite_data=invite_data, invited_by=user)
    return SuccessResponse(
        detail="Приглашение отправлено на электронную почту пользователя, срок действия приглашения 3 дня",
        status=200,
    )


@router.get("/invite/accept/{token}")
async def accept_invite(
    token: str,
    user: Annotated["User", Depends(current_active_user)],
    service: Annotated["InvitationService", Depends(get_invitation_service)],
):
    result = await service.accept_invite(token=token, user=user)
    return result


@router.get("/invite/{invite_id}", response_model=ReadInvite)
async def get_invite_details(
    invite_id: int,
    user: Annotated["User", Depends(current_active_user)],
    service: Annotated["InvitationService", Depends(get_invitation_service)],
):
    result = await service.get_invite(invite_id=invite_id, user=user)
    return result


@router.delete("/invite/{invite_id}")
async def delete_invite(
    invite_id: int,
    user: Annotated["User", Depends(current_active_user)],
    service: Annotated["InvitationService", Depends(get_invitation_service)],
):
    result = await service.delete_invite(invite_id=invite_id, user=user)
    return result
