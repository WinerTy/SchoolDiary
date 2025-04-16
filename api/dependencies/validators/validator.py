from typing import Annotated

from fastapi import Depends

from api.dependencies.repository import get_school_repository
from core.database.crud import SchoolRepository


async def check_school_exists(
    school_id: int,
    school_repo: Annotated["SchoolRepository", Depends(get_school_repository)],
) -> None:
    await school_repo.get_by_id(school_id)
