from typing import TYPE_CHECKING, Annotated, List

from fastapi import APIRouter, Depends, Response, status

from api.dependencies.services.get_service import (
    get_invitation_service,
    get_user_service,
)
from api.v1.auth.fastapi_users import (
    current_active_teacher_or_admin_in_school,
    current_active_user,
)
from core.database.crud.grade.schemas import GradeRead
from core.database.crud.invitation.schemas import (
    CreateInviteResponse,
    ReadInvite,
)
from core.database.crud.user import UserRead
from core.database.crud.user.schemas import UserUpdateRequest
from core.database.schemas import SuccessResponse
from core.services import UserService

if TYPE_CHECKING:
    from core.services.invitation_service import InvitationService
    from core.database import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/invite/", response_model=SuccessResponse)
async def invite_user_for_group(
    invite_data: CreateInviteResponse,
    user: Annotated["User", Depends(current_active_teacher_or_admin_in_school)],
    service: Annotated["InvitationService", Depends(get_invitation_service)],
):
    await service.create_invite(invite_data=invite_data, invited_by=user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


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


@router.get("/me/", response_model=UserRead)
async def read_me(
    user: Annotated["User", Depends(current_active_user)],
):
    return user


@router.patch("/me/", response_model=UserRead)
async def update_me(
    user: Annotated["User", Depends(current_active_user)],
    service: Annotated["UserService", Depends(get_user_service)],
    update_data: UserUpdateRequest,
):
    return await service.update_user(user_id=user.id, update_data=update_data)


@router.get("/grade/", response_model=List[GradeRead])
async def get_my_grades(
    user: Annotated["User", Depends(current_active_user)],
):
    return user.grades
