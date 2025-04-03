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
        "role",
    ]
    fields = [
        "email",
        "first_name",
        "middle_name",
        "last_name",
        "role",
        "classroom",
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
