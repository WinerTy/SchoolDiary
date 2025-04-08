from starlette_admin.contrib.sqla import ModelView


class ClassroomSubjectAdmin(ModelView):
    label = "Предметы в классах"
    name = "Предмет в классе"

    fields = ["classroom", "subject"]
