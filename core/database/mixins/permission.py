from typing import TYPE_CHECKING

from fastapi import HTTPException

if TYPE_CHECKING:
    from core.types import Model


class PermissionMixin:
    @staticmethod
    def validate_record_permission(
        instance: "Model", user_id: int, model_field: str = "user_id"
    ):
        if getattr(instance, model_field) != user_id:
            raise HTTPException(
                detail="You dont have permission for this action",
                status_code=403,
            )
