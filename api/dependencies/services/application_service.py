from typing import Annotated

from fastapi.params import Depends

from api.dependencies.repository import get_application_repository
from core.services.application_service import ApplicationService


async def get_application_service(
    repo: Annotated["ApplicationRepository", Depends(get_application_repository)],
):
    yield ApplicationService(repo)
