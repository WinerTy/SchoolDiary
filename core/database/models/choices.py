from enum import Enum


class ChoicesRole(Enum):
    platform_admin = "platform_admin"
    school_admin = "school_admin"
    teacher = "teacher"
    student = "student"


class ChoicesApplicationStatus(Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
