from typing import Literal

from fastapi import HTTPException

from core.database import School, User
from core.database.crud import BaseValidator


class SchoolValidator(BaseValidator):
    def validate(
        self,
        instance: "Model",
        action: Literal["create", "read", "update", "delete"],
        **kwargs
    ):

        if action == "create":
            self.validate_ownership(instance=instance, user=kwargs.get("user"))

    @staticmethod
    def validate_ownership(instance: "School", user: "User"):
        if instance.director_id != user.id:
            raise HTTPException(status_code=403, detail="You can't create this school")

    @staticmethod
    def validate_teacher(instance: "School", user: "User"):
        pass
