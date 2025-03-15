
from typing import TYPE_CHECKING

from fastapi import HTTPException

from core.database.crud.base import BaseValidator
from core.database.models.choices import ChoicesApplicationStatus

if TYPE_CHECKING:
    from core.database import Applications


class ApplicationValidator(BaseValidator):
    def validate(self, instance: "Applications", **kwargs) -> None:
        user_id = kwargs.get("user_id")
        self._validate_status(instance)
        self._validate_permissions(instance, user_id)

    @staticmethod
    def _validate_status(instance: "Applications"):
        if instance.status != ChoicesApplicationStatus.pending:
            raise HTTPException(status_code=400, detail="Application is not pending")

    @staticmethod
    def _validate_permissions(instance: "Applications", user_id: int):
        if instance.user_id != user_id:
            raise HTTPException(
                status_code=403, detail="You can't update this application"
            )

