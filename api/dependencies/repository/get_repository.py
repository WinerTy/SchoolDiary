from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from core.database.crud import UserRepository, SchoolRepository, ApplicationRepository
from core.database.utils import db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield UserRepository(session)


async def get_school_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield SchoolRepository(db=session)


async def get_application_repository(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    yield ApplicationRepository(db=session)
