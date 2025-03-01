from typing import (
    TYPE_CHECKING,
    Annotated,
)

from fastapi import Depends

from core.database import AccessToken
from core.database.utils import db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_tokens_db(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    yield AccessToken.get_db(session=session)
