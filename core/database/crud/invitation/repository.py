import datetime
import uuid
from typing import TYPE_CHECKING

from fastapi import HTTPException
from sqlalchemy import select

from core.database import Invitation
from core.database.crud.base.repository import BaseRepository
from core.database.models.choices import ChoicesInviteStatus
from .schemas import CreateInvite, ReadInvite, UpdateInvite

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class InvitationRepository(
    BaseRepository[Invitation, CreateInvite, ReadInvite, UpdateInvite]
):
    def __init__(self, db: "AsyncSession"):
        super().__init__(Invitation, db)

    async def get_by_token(self, token: str) -> Invitation:
        stmt = select(self.model).where(Invitation.token == token)
        result = await self.db.execute(stmt)
        instance = result.scalars().first()
        if not instance:
            raise HTTPException(status_code=404, detail="Invitation not found")
        return instance

    async def create_invite_via_token(
        self, user_id: int, invited_by: int
    ) -> Invitation:
        token = str(uuid.uuid4())
        instance = await self.create(
            CreateInvite(user_id=user_id, token=token, invited_by=invited_by)
        )
        return instance

    async def verification_token(self, token: str) -> bool:
        instance = await self.get_by_token(token)
        date = datetime.datetime.now()
        if (
            instance.expires_at < date
            or instance.status == ChoicesInviteStatus.accepted.value
        ):
            raise HTTPException(status_code=400, detail="Token expired or already used")
        return True

    async def change_invite_status(self, token: str) -> Invitation:
        instance = await self.get_by_token(token)
        is_verify = await self.verification_token(token)
        if is_verify:
            update_data = UpdateInvite(status=ChoicesInviteStatus.accepted.value)
            await self.update(instance.id, update_data)
        return instance
