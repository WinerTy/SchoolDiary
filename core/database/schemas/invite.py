from pydantic import BaseModel

from core.database.models.choices import ChoicesInviteStatus


class BaseInvite(BaseModel):
    user_id: int


class ReadInvite(BaseInvite):
    id: int
    token: str


class UpdateInvite(BaseModel):
    status: ChoicesInviteStatus


class CreateInvite(BaseInvite):
    token: str = None
