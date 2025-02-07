from typing import Annotated
from typing import TYPE_CHECKING

from fastapi import Depends

from core.database.crud.school import SchoolRepository
from core.database.utils import db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_school_repo(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield SchoolRepository(db=session)
