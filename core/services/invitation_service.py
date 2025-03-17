from typing import TYPE_CHECKING

from core.database import Invitation, User
from core.database.crud import UserRepository
from core.database.crud.invitation import InvitationRepository
from core.database.crud.invitation.schemas import (
    CreateInvite,
    ReadInvite,
    CreateInviteResponse,
)
from .base_services import BaseService
from ..database.models.choices import ChoicesRole

if TYPE_CHECKING:
    pass


class InvitationService(BaseService[Invitation, CreateInvite, ReadInvite, ReadInvite]):
    def __init__(
        self,
        invitation_repository: InvitationRepository,
        user_repository: UserRepository,
    ):
        super().__init__(
            repositories={"invitation": invitation_repository, "user": user_repository},
        )

    async def accept_invite(self, token: str, user: "User") -> Invitation:
        user_repo = self.get_repo("user")
        invite_repo = self.get_repo("invitation")
        token = await invite_repo.change_invite_status(token, user=user)
        await user_repo.change_user_role(token.user_id, ChoicesRole.student)  # TODO Fix
        return token

    async def get_invite_by_token(self, token: str) -> Invitation | None:
        repo = self.get_repo("invitation")
        return await repo.get_by_token(token)

    async def create_invite(
        self, invite_data: CreateInviteResponse, invited_by: "User"
    ) -> Invitation:
        await self.get_user_by_id(invite_data.user_id)  # for check user record in DB
        repo = self.get_repo("invitation")
        return await repo.create_invite_via_token(invite_data, invited_by)

    async def get_user_by_id(self, user_id: int, repo_name: str = "user"):
        result = await self.get_by_id(user_id, repo_name)
        return result
