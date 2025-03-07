from starlette_admin.contrib.sqla import Admin

from core.app.admin.views import (
    UserAdmin,
    SubjectAdmin,
    TeacherInfoAdmin,
    SchoolAdmin,
    ScheduleAdmin,
    LessonAdmin,
    ClassroomAdmin,
    GradeAdmin,
)
from core.database import (
    User,
    Subject,
    Teacher,
    Classroom,
    School,
    Schedule,
    Lesson,
    Grade,
)
from core.database.utils import db_helper


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
    admin.add_view(TeacherInfoAdmin(Teacher))
    admin.add_view(LessonAdmin(Lesson))
    admin.add_view(ScheduleAdmin(Schedule))
    admin.add_view(SchoolAdmin(School))
    admin.add_view(ClassroomAdmin(Classroom))
    admin.add_view(GradeAdmin(Grade))
    return admin
