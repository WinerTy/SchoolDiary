import uuid
from typing import TYPE_CHECKING

from fastapi import HTTPException
from sqlalchemy import select

from core.database import Invitation
from core.database.crud.base.repository import BaseRepository
from core.database.models.choices import ChoicesInviteStatus
from .schemas import CreateInvite, ReadInvite, UpdateInvite, CreateInviteResponse

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from core.database import User

from .validator import InvitationValidator


class InvitationRepository(
    BaseRepository[Invitation, CreateInvite, ReadInvite, UpdateInvite]
):
    def __init__(self, db: "AsyncSession", validator: "InvitationValidator"):
        super().__init__(Invitation, db)
        self.validator = validator

    async def get_by_token(self, token: str) -> Invitation:
        stmt = select(self.model).where(Invitation.token == token)
        result = await self.db.execute(stmt)
        instance = result.scalars().first()
        if not instance:
            raise HTTPException(status_code=404, detail="Invitation not found")
        return instance

    async def create_invite_via_token(
        self, invite_data: CreateInviteResponse, invited_by: "User"
    ) -> Invitation:
        self.validator.create_validation(invited_by, invite_data.role)
        token = str(uuid.uuid4())
        instance = await self.create(
            CreateInvite(
                user_id=invite_data.user_id,
                invite_role=invite_data.role,
                token=token,
                invited_by=invited_by.id,
            )
        )
        return instance

    async def change_invite_status(self, token: str) -> Invitation:
        instance = await self.get_by_token(token)
        self.validator.validate(instance)
        update_data = UpdateInvite(status=ChoicesInviteStatus.accepted.value)
        await self.update(instance.id, update_data)
        return instance
