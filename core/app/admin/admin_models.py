from starlette_admin.contrib.sqla import ModelView

from core.database import User


# class ScheduleAdmin(ModelView(Schedule)):
#     column_list = [
#         Schedule.id,
#         Schedule.classroom,
#     ]
#
#
# class LessonAdmin(ModelView(Lesson)):
#     column_list = [
#         Lesson.id,
#         Lesson.subject,
#         Lesson.teacher,
#         Lesson.start_time,
#         Lesson.end_time,
#         Lesson.additional_info,
#     ]
#
#     form_columns = [
#         "subject",
#         "teacher",
#         "schedule",
#         Lesson.start_time,
#         Lesson.end_time,
#         Lesson.additional_info,
#     ]
#
#     form_ajax_refs = {
#         "subject": {"fields": ["subject_name"]},
#         "teacher": {"fields": ["first_name", "last_name"]},
#     }
#
#
# class SubjectAdmin(ModelView, model=Subject):
#     column_list = [
#         Subject.id,
#         Subject.subject_name,
#     ]
#
#
# class TeacherAdmin(ModelView, model=Teacher):
#     column_list = [
#         Teacher.id,
#         "user",
#         Teacher.subject,
#     ]
#
#
# class InvitationAdmin(ModelView, model=Invitation):
#     column_list = [
#         Invitation.id,
#         Invitation.user_id,
#         Invitation.token,
#         Invitation.created_at,
#         Invitation.expires_at,
#         Invitation.status,
#     ]
#
#     name_plural = "Приглашения"


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

    sortable_fields = [User.role]


# class SchoolAdmin(ModelView, model=School):
#     column_list = [
#         School.id,
#         School.school_address,
#         School.school_description,
#         School.school_type,
#         School.school_phone,
#         School.director,
#         School.teachers,
#     ]
#     form_columns = [
#         School.school_name,
#         School.school_address,
#         School.school_description,
#         School.school_type,
#         School.school_phone,
#         "director",
#         "teachers",
#     ]
#     column_details_exclude_list = [School.director_id]
#
#     form_ajax_refs = {
#         "director": {
#             "fields": ("first_name", "last_name"),
#             "order_by": "first_name",
#             "formatter": lambda model: (model.full_name if model else None),
#         },
#         "teachers": {
#             "fields": ("first_name", "last_name"),
#             "order_by": "first_name",
#             "multiple": True,
#             "formatter": lambda model: (model.full_name if model else None),
#         },
#     }
#
#     # Переименование колонок для более понятного интерфейса
#     column_labels = {
#         "director": "Директор",
#         "teachers": "Учителя",
#     }
#
#     name_plural = "Школы"
#
#     async def on_model_change(
#         self, data: dict, model: Any, is_created: bool, request: Request
#     ) -> None:
#         print("on_model_change", data)
#
#
# class ClassroomAdmin(ModelView, model=Classroom):
#     column_list = [
#         Classroom.id,
#         Classroom.class_name,
#         Classroom.class_teacher,
#         Classroom.students,
#     ]
#
#     form_columns = [
#         Classroom.class_name,
#         Classroom.year_of_graduation,
#         Classroom.is_graduated,
#         "school",
#         "class_teacher",
#         "students",
#     ]
#
#     form_ajax_refs = {
#         "school": {
#             "fields": ("school_name",),
#             "order_by": "school_name",
#             "formatter": lambda model: (model.school_name if model else None),
#         },
#         "class_teacher": {
#             "fields": ("first_name", "last_name"),
#             "order_by": "first_name",
#             "formatter": lambda model: (model.full_name if model else None),
#             "filters": {
#                 "role": ChoicesRole.teacher.value,
#                 "school_id": lambda model: print(model)
#                 or (model.school_id if model else None),
#             },
#         },
#         "students": {
#             "fields": ("first_name", "last_name"),
#             "order_by": "first_name",
#             "multiple": True,
#             "formatter": lambda model: (model.full_name if model else None),
#             "filters": {
#                 "role": ChoicesRole.student.value,
#                 "school_id": lambda model: model.school_id if model else None,
#             },
#         },
#     }
