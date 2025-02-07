from typing import Any

from core.database import Applications
from core.database.schemas.application import ReadApplication, CreateApplication
from core.services.base_services import BaseService


class ApplicationService(
    BaseService[Applications, CreateApplication, ReadApplication, ReadApplication]
):
    def __init__(self, repo: Any):
        super().__init__(repo)
