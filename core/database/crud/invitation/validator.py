from datetime import datetime
from typing import TYPE_CHECKING

from fastapi import HTTPException

from core.database.crud.base import BaseValidator
from core.database.models.choices import ChoicesInviteStatus

if TYPE_CHECKING:
    from core.database import User, Invitation


class InvitationValidator(BaseValidator):
    def validate(self, instance: "Invitation", **kwargs):
        self.validate_expires_date(instance)

    @staticmethod
    def validate_expires_date(instance: "Invitation"):
        date = datetime.now()
        if (
            instance.expires_at < date
            or instance.status == ChoicesInviteStatus.accepted.value
        ):
            raise HTTPException(status_code=400, detail="Token expired or already used")

    def validate_user_permission(self, user: "User"):
        pass
