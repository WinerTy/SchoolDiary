from typing import TYPE_CHECKING

from sqladmin import Admin

from core.database.utils import db_helper
from .admin_models import (
    UserAdmin,
    SchoolAdmin,
    ClassroomAdmin,
    InvitationAdmin,
    TeacherAdmin,
    SubjectAdmin,
    ScheduleAdmin,
    LessonAdmin,
)

if TYPE_CHECKING:
    from fastapi import FastAPI


def create_admin_app(app: "FastAPI", authentication_backend) -> None:
    admin = Admin(app, db_helper.engine)

    admin.add_view(UserAdmin)
    admin.add_view(SchoolAdmin)
    admin.add_view(ClassroomAdmin)
    admin.add_view(InvitationAdmin)
    admin.add_view(TeacherAdmin)
    admin.add_view(SubjectAdmin)
    admin.add_view(ScheduleAdmin)
    admin.add_view(LessonAdmin)
