from core.database import Applications
from core.database.crud.base_repo import BaseRepository
from core.database.schemas.application import ReadApplication, CreateApplication
from core.services.base_services import BaseService
from core.types import Model, CreateSchema, ReadSchema


class ApplicationService(
    BaseService[Applications, CreateApplication, ReadApplication, ReadApplication]
):
    def __init__(
        self, repository: BaseRepository[Model, CreateSchema, ReadSchema, ReadSchema]
    ):
        super().__init__(repository)
