from abc import ABC
from typing import TypeVar, Generic, Optional, List, Dict, Any

from core.database.crud.base.repository import BaseRepository
from core.types import Model, CreateSchema, ReadSchema, UpdateSchema

RepositoryType = TypeVar("RepositoryType", bound=BaseRepository[Any, Any, Any, Any])
ServiceType = TypeVar("ServiceType", bound="BaseService[Any, Any, Any, Any]")


class BaseService(Generic[Model, CreateSchema, ReadSchema, UpdateSchema], ABC):
    def __init__(
        self,
        repositories: Dict[str, RepositoryType],
        services: Optional[Dict[str, ServiceType]] = None,
    ):
        self.repositories = repositories
        self.services = services

    def get_service(self, service_name: str) -> ServiceType:
        """Get service by name."""
        service = self.services.get(service_name)
        if not service:
            raise ValueError(f"Service {service_name} not found")
        return service

    def get_repo(self, repo_name: str = None) -> RepositoryType:
        if repo_name is None:
            if not self.repositories:
                raise ValueError("No repositories available")
            return next(iter(self.repositories.values()))

        repo = self.repositories.get(repo_name)
        if not repo:
            raise ValueError(f"Repository {repo_name} not found")
        return repo

    async def get_by_id(self, item_id: int, repo_name: str = None) -> Optional["Model"]:
        repo = self.get_repo(repo_name)
        return await repo.get_by_id(item_id)

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        repo_name: str = None,
    ) -> List["Model"]:
        repo = self.get_repo(repo_name)
        return await repo.get_all()

    async def create(
        self, item: CreateSchema, repo_name: str = None, **kwargs
    ) -> "Model":
        try:
            repo = self.get_repo(repo_name)
            return await repo.create(item, **kwargs)
        except Exception as e:
            raise e

    async def update(
        self,
        item_id: int,
        item: CreateSchema,
        repo_name: str = None,
    ) -> Model:
        repo = self.get_repo(repo_name)
        return await repo.update(item_id, item)
