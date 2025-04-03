from typing import Dict, Any

from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError
from starlette.requests import Request
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.exceptions import FormValidationError

from core.database import School
from core.database.utils import db_helper


class SchoolAdmin(ModelView):
    label = "Школы"
    name = "Школа"

    column_visibility = ["id", "school_name"]

    fields = [
        "school_name",
        "school_address",
        "school_description",
        "school_type",
        "school_phone",
        "director",
    ]

    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        errors = {}
        director = data.get("director")

        if not director:
            errors["director"] = "Выберите директора школы"
        elif await self._is_director_associated(director.id):
            errors["director"] = "Этот директор уже привязан к другой школе"

        if errors:
            raise FormValidationError(errors)

        await super().validate(request, data)

    async def on_model_change(self, data, model, is_created):
        try:
            await super().on_model_change(data, model, is_created)
        except IntegrityError as e:
            if "uq_school_director_id" in str(e):
                raise FormValidationError(
                    {"director": "Этот директор уже привязан к другой школе"}
                )
            raise

    @staticmethod
    async def _is_director_associated(director_id: int) -> bool:
        """Проверяет, есть ли у директора уже привязанная школа"""
        async with db_helper.session_factory() as session:
            stmt = select(exists().where(School.director_id == director_id))
            return await session.scalar(stmt)
