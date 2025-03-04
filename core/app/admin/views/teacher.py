from starlette_admin.contrib.sqla import ModelView


class TeacherInfoAdmin(ModelView):
    label = "Информация о преподавателе"
    name = "Информация о преподавателе"

    column_visibility = ["id", "subject"]
