from typing import TYPE_CHECKING

from core.database import SchoolSubject
from core.database.crud import BaseRepository
from .schemas import SchoolSubjectCreate, SchoolSubjectUpdate, SchoolSubjectRead

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SchoolSubjectRepository(
    BaseRepository[
        SchoolSubject, SchoolSubjectCreate, SchoolSubjectUpdate, SchoolSubjectRead
    ]
):
    def __init__(self, db: "AsyncSession"):
        super().__init__(SchoolSubject, db)
