from typing import TYPE_CHECKING, Set

from sqlalchemy import select

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

    async def get_by_ids(self, ids: Set[int]) -> Set[int]:
        if not ids:
            return set()

        stmt = select(self.model.id).where(self.model.id.in_(ids))
        result = await self.db.execute(stmt)
        return {row[0] for row in result}
