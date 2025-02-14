from sqladmin import ModelView

from core.database import User, School


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.role,
        User.school_id,
        User.school,  # Отображаем связь с School
    ]
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

    form_ajax_refs = {
        "director": {
            "fields": ("email",),
            "order_by": "email",
        },
        "teachers": {
            "fields": ("email",),
            "order_by": "email",
            "multiple": True,
        },
    }

    column_labels = [{""}]
