__all__ = [
    "UserAdmin",
    "SubjectAdmin",
    "TeacherInfoAdmin",
    "SchoolAdmin",
    "ClassroomAdmin",
    "LessonAdmin",
    "ScheduleAdmin",
]

from .classroom import ClassroomAdmin
from .lesson import LessonAdmin
from .schedule import ScheduleAdmin
from .school import SchoolAdmin
from .subject import SubjectAdmin
from .teacher import TeacherInfoAdmin
from .user import UserAdmin
