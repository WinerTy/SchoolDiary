from starlette_admin.contrib.sqla import ModelView

from core.database import User, School


class UserAdmin(ModelView):
    label = "Пользователи"
    name = "Пользователя"

    column_visibility = [
        "id",
        "email",
        "first_name",
        "middle_name",
        "last_name",
    ]
    fields = ["email", "first_name", "middle_name", "last_name", "role"]

    column_details_list = [
        "id",
        "email",
        "first_name",
        "middle_name",
        "last_name",
        "role",
    ]

    sortable_fields = [User.role]


class SubjectAdmin(ModelView):
    label = "Предметы"
    name = "Предмет"

    column_visibility = ["id", "subject_name"]

    fields = ["subject_name", "lessons"]


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
    ]


class ScheduleAdmin(ModelView):
    label = "Расписание"
    name = "Расписание"

    column_visibility = ["id", "classroom", "schedule_date"]

    fields = ["classroom", "schedule_date", "lessons"]


class SchoolAdmin(ModelView):
    label = "Школы"
    name = "Школа"

    column_visibility = ["id", "school_name"]

    fields = ["school_name", School.school_phone]


class ClassroomAdmin(ModelView):
    label = "Классы"
    name = "Класс"

    # Указываем, какие колонки отображать
    column_list = [
        "id",
        "class_name",
        School,
        "year_of_graduation",
        "is_graduated",
    ]

    # Указываем поля для редактирования
    fields = [
        "class_name",
        "school",
        "schedules",
        "year_of_graduation",
        "is_graduated",
    ]

    column_labels = {
        "is_graduated": "Выпускник",
    }
