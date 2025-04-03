from starlette_admin.contrib.sqla.ext.pydantic import ModelView


class SubjectAdmin(ModelView):
    label = "Предметы"
    name = "Предмет"

    column_visibility = ["id", "subject_name"]

    fields = [
        "subject_name",
    ]
