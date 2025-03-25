from datetime import datetime
from typing import TYPE_CHECKING

from core.database import Invitation, User
from core.database.crud import UserRepository
from core.database.crud.invitation import InvitationRepository
from core.database.crud.invitation.schemas import (
    CreateInvite,
    ReadInvite,
    CreateInviteResponse,
)
from smtp.schemas import EmailSchema
from smtp.service import SMTPService
from .base_services import BaseService

if TYPE_CHECKING:
    pass


class InvitationService(BaseService[Invitation, CreateInvite, ReadInvite, ReadInvite]):
    def __init__(
        self,
        invitation_repository: InvitationRepository,
        user_repository: UserRepository,
        smtp: "SMTPService",
    ):
        self.smtp = smtp
        super().__init__(
            repositories={"invitation": invitation_repository, "user": user_repository},
        )

    async def accept_invite(self, token: str, user: "User") -> Invitation:
        user_repo = self.get_repo("user")
        invite_repo = self.get_repo("invitation")
        invite = await invite_repo.change_invite_status(token, user=user)
        await user_repo.change_user_role(invite.user_id, invite.invite_role)
        return invite

    async def get_invite_by_token(self, token: str) -> Invitation | None:
        repo = self.get_repo("invitation")
        return await repo.get_by_token(token)

    async def create_invite(
        self,
        invite_data: CreateInviteResponse,
        invited_by: "User",
    ) -> Invitation:
        user = await self.get_user_by_id(invite_data.user_id)
        repo = self.get_repo("invitation")
        invite: Invitation = await repo.create_invite_via_token(invite_data, invited_by)
        await self.smtp.send_email(
            subject="Вас пригласили",
            email_content=EmailSchema(
                email=[user.email],
                body={
                    "role": invite.invite_role.value,
                    "recipient_name": user.full_name,
                    "url": f"http://localhost:8000/api/users/invite/accept/{invite.token}",
                    "date": datetime.today(),
                },
            ),
            template_name="invite_email.html",
        )
        return invite

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.get_by_id(user_id, repo_name="user")

    async def get_invite(self, invite_id: int, user: "User") -> Invitation:
        repo = self.get_repo("invitation")
        return await repo.get_invite_by_id(invite_id, user)

    async def delete_invite(self, invite_id: int, user: "User") -> None:
        repo: InvitationRepository = self.get_repo("invitation")
        await repo.delete_invite(invite_id, user)
