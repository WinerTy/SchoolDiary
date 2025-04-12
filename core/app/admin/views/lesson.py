from typing import Dict, Any

from starlette.requests import Request
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.exceptions import FormValidationError

from core.database import Schedule, Lesson


class LessonAdmin(ModelView):
    label = "Уроки"
    name = "Урок"

    column_visibility = ["id"]

    fields = [
        "id",
        "teacher",
        "start_time",
        "end_time",
        "additional_info",
        "schedule",
        "school_subjects",
    ]

    def get_list_query(self):
        return super().get_list_query().order_by("start_time", "end_time")

    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        errors = {}

        start_time = data.get("start_time")
        end_time = data.get("end_time")
        if end_time <= start_time:
            errors["end_time"] = "end_time должен быть позже start_time"

        if errors:
            raise FormValidationError(errors)

        return await super().validate(request, data)

    async def before_create(
        self, request: Request, data: Dict[str, Any], obj: Lesson
    ) -> None:

        schedule: Schedule = data.get("schedule")

        if schedule.count_lessons() > 8:
            raise FormValidationError({"schedule": "Расписание заполнено"})

        valid, lesson = schedule.validate_lessons(new_lessons=obj)
        if not valid:
            raise FormValidationError(
                {
                    "start_time": f"Урок пересекается с другим уроком. {lesson.school_subjects.subject_name}: {lesson.id}",
                    "end_time": f"Урок пересекается с другим уроком. {lesson.school_subjects.subject_name}: Id: {lesson.id}",
                }
            )

        await super().before_create(request, data, obj)
