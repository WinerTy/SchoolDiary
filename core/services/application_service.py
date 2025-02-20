from core.database import Applications
from core.database.crud.base_repo import BaseRepository
from core.database.schemas.application import ReadApplication, CreateApplication
from core.services.base_services import BaseService


class ApplicationService(
    BaseService[Applications, CreateApplication, ReadApplication, ReadApplication]
):
    def __init__(self, application_repo: BaseRepository):
        super().__init__(repositories={"application": application_repo})
