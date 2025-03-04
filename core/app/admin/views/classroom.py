from starlette_admin.contrib.sqla import ModelView


class ClassroomAdmin(ModelView):
    label = "Классы"
    name = "Класс"

    # Указываем, какие колонки отображать
    column_list = [
        "id",
        "class_name",
        "school",
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
        "students",
    ]

    column_labels = {
        "is_graduated": "Выпускник",
    }
