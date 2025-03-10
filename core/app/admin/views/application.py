from starlette_admin.contrib.sqla import ModelView


class ApplicationAdmin(ModelView):

    label = "Заявки"
    name = "Заявка"

    column_visibility = [
        "id",
        "director_full_name",
        "director_phone",
        "director_email",
        "created_at",
        "status",
    ]

    fields = column_visibility
