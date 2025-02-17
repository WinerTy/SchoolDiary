from typing import TYPE_CHECKING

from core.database import Invitation
from core.database.crud import UserRepository
from core.database.crud.invitation_repo import InvitationRepository
from core.database.schemas.invite import CreateInvite, ReadInvite
from .base_services import BaseService

if TYPE_CHECKING:
    pass


class InvitationService(BaseService[Invitation, CreateInvite, ReadInvite, ReadInvite]):
    def __init__(
        self,
        invitation_repository: InvitationRepository,
        user_repository: UserRepository,
    ):
        super().__init__(
            repository=invitation_repository,
            repositories={"invitation": invitation_repository, "user": user_repository},
        )

    async def accept_invite(self, user_id: int, token: str):
        user_repo = self.get_repo("user")
        invite_repo = self.get_repo("invitation")
        user = await user_repo.get_by_id(user_id)

    async def get_invite_by_token(self, token: str) -> Invitation | None:
        repo = self.get_repo("invitation")
        return await repo.get_by_token(token)

    async def create_invite(self, user_id) -> Invitation:
        repo = self.get_repo("invitation")
        return await repo.create_invite_via_token(user_id)

    async def get_user_by_id(self, user_id: int, repo_name: str = "user"):
        result = await self.get_by_id(user_id, repo_name)
        return result
