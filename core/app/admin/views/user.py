from starlette_admin.contrib.sqla import ModelView


class UserAdmin(ModelView):
    label = "Пользователи"
    name = "Пользователя"

    column_visibility = [
        "id",
        "email",
        "first_name",
        "middle_name",
        "last_name",
        "teacher_info",
        "role",
    ]
    fields = [
        "email",
        "first_name",
        "middle_name",
        "last_name",
        "role",
        "classroom",
        "teacher_info",
    ]

    column_details_list = [
        "id",
        "email",
        "first_name",
        "middle_name",
        "last_name",
        "role",
        "classroom",
    ]
