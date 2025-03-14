from starlette_admin.contrib.sqla import ModelView


class SchoolAdmin(ModelView):
    label = "Школы"
    name = "Школа"

    column_visibility = ["id", "school_name"]

    fields = ["school_name", "school_phone"]
