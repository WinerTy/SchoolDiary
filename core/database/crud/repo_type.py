from typing import TypeVar

from core.database.crud.base.repository import BaseRepository

RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)
