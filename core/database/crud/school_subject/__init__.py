__all__ = [
    "SchoolSubjectUpdate",
    "SchoolSubjectCreate",
    "SchoolSubjectRead",
    "SchoolSubjectCreateRequest",
    "SchoolSubjectRepository",
]

from .repository import SchoolSubjectRepository
from .schemas import (
    SchoolSubjectUpdate,
    SchoolSubjectCreate,
    SchoolSubjectRead,
    SchoolSubjectCreateRequest,
)
