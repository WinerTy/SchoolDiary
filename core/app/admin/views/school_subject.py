from typing import Dict, Any

from fastapi import Request
from sqlalchemy import select, exists
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.exceptions import FormValidationError

from core.database import SchoolSubject
from core.database.utils import db_helper


class SchoolSubjectAdmin(ModelView):
    label = "Предметы школы"
    name = "Предмет школы"

    fields = [
        "school",
        "subject_name",
    ]
    sortable_fields = ["school"]
    fields_default_sort = ("school", "asc")

    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        await super().validate(request, data)  # Стандартная валидация
        # Проверка уникальности
        school = data.get("school")
        subject_name = data.get("subject_name")

        # Валидация длины названия
        if len(subject_name) < 3:
            raise FormValidationError(
                {"subject_name": "Название предмета должно быть не менее 3 символов"}
            )

        if school and subject_name:
            async with db_helper.session_factory() as session:
                exists_query = select(
                    exists().where(
                        SchoolSubject.school_id == school.id,
                        SchoolSubject.subject_name == subject_name,
                    )
                )
                if await session.scalar(exists_query):
                    raise FormValidationError(
                        {
                            "subject_name": "Предмет с таким названием уже существует в этой школе"
                        }
                    )
