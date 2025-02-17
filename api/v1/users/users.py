from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import Response

from api.dependencies.services.application_service import get_invitation_service
from core.database.schemas.invite import CreateInvite

if TYPE_CHECKING:
    from core.services.invitation_service import InvitationService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
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
    repo = service.get_repo()
    result = await repo.change_invite_status(token=token)
    print(result)
    return result
