from starlette_admin.contrib.sqla import Admin

from core.app.admin.views import (
    UserAdmin,
    SchoolAdmin,
    ScheduleAdmin,
    LessonAdmin,
    ClassroomAdmin,
    GradeAdmin,
    ApplicationAdmin,
    SchoolSubjectAdmin,
)
from core.database import (
    User,
    Classroom,
    School,
    Schedule,
    Lesson,
    Grade,
    Applications,
    SchoolSubject,
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
    # admin.add_view(SubjectAdmin(Subject, pydantic_model=SubjectAdminSchema))
    # admin.add_view(TeacherInfoAdmin(Teacher))
    admin.add_view(ApplicationAdmin(Applications))
    admin.add_view(SchoolAdmin(School))
    admin.add_view(SchoolSubjectAdmin(SchoolSubject))
    admin.add_view(ClassroomAdmin(Classroom))
    admin.add_view(ScheduleAdmin(Schedule))
    admin.add_view(LessonAdmin(Lesson))
    admin.add_view(GradeAdmin(Grade))
    return admin
