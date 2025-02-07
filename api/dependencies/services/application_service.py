from typing import Annotated

from fastapi.params import Depends

from api.dependencies.repo.application_repo import get_application_repo
from core.services.application_service import ApplicationService


async def get_application_service(
    repo: Annotated["ApplicationRepository", Depends(get_application_repo)],
):
    yield ApplicationService(repo)
