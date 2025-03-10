from typing import TYPE_CHECKING, List

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from core.database import Subject
from core.database.crud.base_repo import BaseRepository
from core.database.schemas import SuccessResponse
from core.database.schemas.subject import CreateSubject, ReadSubject, UpdateSubject

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SubjectRepository(
    BaseRepository[Subject, CreateSubject, ReadSubject, UpdateSubject]
):
    def __init__(self, db: "AsyncSession"):
        super().__init__(Subject, db)

    async def create_subjects(self, subjects: List[CreateSubject]) -> SuccessResponse:
        if not subjects:
            raise HTTPException(status_code=400, detail="No subjects provided")
        try:
            db_subjects = [self.model(**subject.model_dump()) for subject in subjects]
            self.db.add_all(db_subjects)
            await self.db.commit()
            return SuccessResponse(detail="Subjects created successfully", status=201)
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Subject already exists")
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
