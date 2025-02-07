from abc import ABC
from typing import Generic, Any, Optional, List

from core.types import Model, CreateSchema, ReadSchema, ResponseSchema


class BaseService(Generic[Model, CreateSchema, ReadSchema, ResponseSchema], ABC):
    def __init__(self, repository: Any):
        self.repository = repository

    async def get_by_id(self, item_id: int) -> Optional[Model]:
        return await self.repository.get_by_id(item_id)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Model]:
        return await self.repository.get_all(skip=skip, limit=limit)

    async def create(self, item: CreateSchema, **kwargs) -> Model:
        return await self.repository.create(item, **kwargs)
