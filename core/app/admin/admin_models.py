from typing import Any

from sqladmin import ModelView
from starlette.requests import Request

from core.database import User, School, Classroom
from core.database.models.choices import ChoicesRole


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.role, User.school_id, User.school, "full_name"]
    form_columns = [
        User.role,
        User.school_id,
    ]
    column_details_exclude_list = [User.hashed_password]  # Скрываем пароль


class SchoolAdmin(ModelView, model=School):
    column_list = [
        School.id,
        School.school_address,
        School.school_description,
        School.school_type,
        School.school_phone,
        School.director,
        School.teachers,
    ]
    form_columns = [
        School.school_name,
        School.school_address,
        School.school_description,
        School.school_type,
        School.school_phone,
        "director",
        "teachers",
    ]
    column_details_exclude_list = [School.director_id]

    form_ajax_refs = {
        "director": {
            "fields": ("first_name", "last_name"),
            "order_by": "first_name",
            "formatter": lambda model: (model.full_name if model else None),
        },
        "teachers": {
            "fields": ("first_name", "last_name"),
            "order_by": "first_name",
            "multiple": True,
            "formatter": lambda model: (model.full_name if model else None),
        },
    }

    # Переименование колонок для более понятного интерфейса
    column_labels = {
        "director": "Директор",
        "teachers": "Учителя",
    }

    name_plural = "Школы"

    async def on_model_change(
        self, data: dict, model: Any, is_created: bool, request: Request
    ) -> None:
        print("on_model_change", data)


class ClassroomAdmin(ModelView, model=Classroom):
    column_list = [
        Classroom.id,
        Classroom.class_name,
        Classroom.class_teacher,
        Classroom.students,
    ]

    form_columns = [
        Classroom.class_name,
        "school",
        "class_teacher",
        "students",
    ]

    form_ajax_refs = {
        "school": {
            "fields": ("school_name",),
            "order_by": "school_name",
            "formatter": lambda model: (model.school_name if model else None),
        },
        "class_teacher": {
            "fields": ("first_name", "last_name"),
            "order_by": "first_name",
            "formatter": lambda model: (model.full_name if model else None),
            "filters": {
                "role": ChoicesRole.teacher.value,
                "school_id": lambda model: print(model)
                or (model.school_id if model else None),
            },
        },
        "students": {
            "fields": ("first_name", "last_name"),
            "order_by": "first_name",
            "multiple": True,
            "formatter": lambda model: (model.full_name if model else None),
            "filters": {
                "role": ChoicesRole.student.value,
                "school_id": lambda model: model.school_id if model else None,
            },
        },
    }
