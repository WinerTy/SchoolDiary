from starlette_admin.contrib.sqla import ModelView


class ScheduleAdmin(ModelView):
    label = "Расписание"
    name = "Расписание"

    column_visibility = ["id", "classroom", "schedule_date"]

    fields = ["classroom", "schedule_date", "lessons"]
