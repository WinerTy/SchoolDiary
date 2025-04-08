__all__ = [
    "UserAdmin",
    "TeacherInfoAdmin",
    "SchoolAdmin",
    "ClassroomAdmin",
    "LessonAdmin",
    "ScheduleAdmin",
    "GradeAdmin",
    "ApplicationAdmin",
    "SchoolSubjectAdmin",
]

from .application import ApplicationAdmin
from .classroom import ClassroomAdmin
from .grade import GradeAdmin
from .lesson import LessonAdmin
from .schedule import ScheduleAdmin
from .school import SchoolAdmin
from .school_subject import SchoolSubjectAdmin
from .teacher import TeacherInfoAdmin
from .user import UserAdmin
