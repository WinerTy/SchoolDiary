from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Grade
from core.database.crud import BaseRepository
from .schemas import GradeCreate, GradeRead


class GradeRepository(BaseRepository[Grade, GradeCreate, GradeRead, GradeCreate]):
    def __init__(self, db: AsyncSession):
        super().__init__(Grade, db)
