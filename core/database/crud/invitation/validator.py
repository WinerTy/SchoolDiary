from datetime import datetime
from typing import TYPE_CHECKING

from fastapi import HTTPException

from core.database.crud.base import BaseValidator
from core.database.models.choices import ChoicesInviteStatus, ChoicesRole

if TYPE_CHECKING:
    from core.database import User, Invitation


class InvitationValidator(BaseValidator):
    def validate(self, instance: "Invitation", **kwargs):
        self.validate_expires_date(instance)

    def create_validation(self, user: "User", invite_role: ChoicesRole, **kwargs):
        self.validate_user_permission(user, invite_role)

    def update_validate(self, **kwargs):
        pass

    @staticmethod
    def validate_expires_date(instance: "Invitation"):
        date = datetime.now()
        if (
            instance.expires_at < date
            or instance.status == ChoicesInviteStatus.accepted.value
        ):
            raise HTTPException(status_code=400, detail="Token expired or already used")

    @staticmethod
    def validate_user_permission(user: "User", invite_role: ChoicesRole):
        if user.role != ChoicesRole.school_admin and invite_role == ChoicesRole.teacher:
            raise HTTPException(detail="You dont have permission", status_code=403)
