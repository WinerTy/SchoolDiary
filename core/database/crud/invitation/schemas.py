from typing import Literal

from pydantic import BaseModel

from core.database.models.choices import ChoicesInviteStatus, ChoicesRole


class BaseInvite(BaseModel):
    user_id: int


class ReadInvite(BaseInvite):
    id: int
    token: str


class UpdateInvite(BaseModel):
    status: ChoicesInviteStatus


class CreateInvite(BaseInvite):
    token: str
    invited_by: int
    invite_role: Literal[ChoicesRole.teacher, ChoicesRole.student]


class CreateInviteResponse(BaseModel):
    user_id: int
    role: Literal[ChoicesRole.teacher, ChoicesRole.student]
