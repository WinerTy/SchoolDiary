from core.database import School
from core.database.crud.base_repo import BaseRepository
from core.database.schemas.school import CreateSchool, ReadSchool
from core.types import Model, CreateSchema, ReadSchema, ResponseSchema
from .base_services import BaseService


class SchoolService(BaseService[School, CreateSchool, ReadSchool, ReadSchool]):
    def __init__(
        self,
        repository: BaseRepository[Model, CreateSchema, ReadSchema, ResponseSchema],
    ):
        super().__init__(repository)
