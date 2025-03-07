from starlette_admin.contrib.sqla import ModelView


class GradeAdmin(ModelView):
    label = "Оценки"
    name = "Оценка"

    column_list = ["id", "user", "lesson", "grade", "additional_info"]
