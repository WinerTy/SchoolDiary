from typing import TypeVar

from .base_repo import BaseRepository

RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)
