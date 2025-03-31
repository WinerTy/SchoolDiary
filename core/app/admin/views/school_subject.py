from starlette_admin.contrib.sqla import ModelView


class SchoolSubjectAdmin(ModelView):
    label = "Предметы школы"
    name = "Предмет школы"



    fields = [
        "school",
        "subject_name",
    ]
