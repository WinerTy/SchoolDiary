from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from core.database.crud.application_repo import ApplicationRepository
from core.database.utils import db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_application_repo(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    yield ApplicationRepository(db=session)
