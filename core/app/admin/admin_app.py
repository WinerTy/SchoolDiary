from starlette_admin.contrib.sqla import Admin

from core.database import User, Subject, Lesson, School, Classroom, Schedule
from core.database.utils import db_helper
from .admin_models import (
    UserAdmin,
    SubjectAdmin,
    LessonAdmin,
    SchoolAdmin,
    ClassroomAdmin,
    ScheduleAdmin,
)


def create_admin_app() -> Admin:
    admin = Admin(
        db_helper.engine,
        title="Admin Panel",
        # auth_provider=AdminAuthProvider(),
        # middlewares=[Middleware(SessionMiddleware, secret_key=config.auth.secret)],
        statics_dir="static",
    )

    admin.add_view(UserAdmin(User))
    admin.add_view(SubjectAdmin(Subject))
    admin.add_view(LessonAdmin(Lesson))
    admin.add_view(ScheduleAdmin(Schedule))
    admin.add_view(SchoolAdmin(School))
    admin.add_view(ClassroomAdmin(Classroom))

    # admin.add_view(SchoolAdmin)
    # admin.add_view(ClassroomAdmin)
    # admin.add_view(InvitationAdmin)
    # admin.add_view(TeacherAdmin)
    # admin.add_view(SubjectAdmin)
    # admin.add_view(ScheduleAdmin)
    # admin.add_view(LessonAdmin)
    return admin
