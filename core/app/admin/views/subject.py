from starlette_admin.contrib.sqla import ModelView


class SubjectAdmin(ModelView):
    label = "Предметы"
    name = "Предмет"

    column_visibility = ["id", "subject_name"]

    fields = ["subject_name", "lessons"]
