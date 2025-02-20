from enum import Enum


class ChoicesRole(str, Enum):
    platform_admin = "platform_admin"
    school_admin = "school_admin"
    class_teacher = "class_teacher"
    teacher = "teacher"
    student = "student"
    user = "user"


class ChoicesApplicationStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ChoicesInviteStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    canceled = "canceled"


class ChoicesDayOfWeek(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"
