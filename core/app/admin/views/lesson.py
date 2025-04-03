from starlette_admin.contrib.sqla import ModelView


class LessonAdmin(ModelView):
    label = "Уроки"
    name = "Урок"

    column_visibility = []

    fields = [
        "subject",
        "teacher",
        "start_time",
        "end_time",
        "additional_info",
        "schedule",
        "school_subjects",
    ]
