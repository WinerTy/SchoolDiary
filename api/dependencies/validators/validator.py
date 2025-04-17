from typing import Annotated

from fastapi import Depends

from api.dependencies.repository import get_school_repository
from core.database.crud import SchoolRepository


async def check_school_exists(
    school_id: int,
    school_repo: Annotated["SchoolRepository", Depends(get_school_repository)],
) -> None:
    """
    Зависимость на проверку существования школы.

    Args:
        school_id: ID школы.
        school_repo: Репозиторий для работы с таблицей.

    Returns:
        None.

    Raises:
        HTTPException: 404 если школа не найдена.
    """
    await school_repo.get_by_id(school_id)
