from datetime import datetime
from typing import TYPE_CHECKING, Literal

from fastapi import HTTPException

from core.database.crud.base import BaseValidator
from core.database.mixins import PermissionMixin
from core.database.models.choices import ChoicesInviteStatus, ChoicesRole

if TYPE_CHECKING:
    from .schemas import CreateInviteResponse
    from core.database import User, Invitation


class InvitationValidator(BaseValidator, PermissionMixin):
    def validate(
        self,
        action: Literal["create", "read", "update", "delete"],
        instance: "Invitation" = None,
        **kwargs
    ):
        user: "User" = kwargs.get("user")

        if action == "create":
            create_data: "CreateInviteResponse" = kwargs.get("create_data")
            self.validate_user_permission(user, create_data.role)

        if action == "update":
            self.validate_expires_date(instance)
            self.validate_record_permission(instance=instance, user_id=user.id)

        if action == "read":
            self.validate_record_permission(
                instance=instance, user_id=user.id, model_field="invited_by"
            )

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
            raise HTTPException(
                detail="You dont have permission for this action", status_code=403
            )
