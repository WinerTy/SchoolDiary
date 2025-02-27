from typing import Annotated, TYPE_CHECKING

from fastapi.params import Depends

from api.dependencies.repository import (
    get_application_repository,
    get_user_repository,
    get_invitation_repository,
    get_school_repository,
    get_subject_repository,
)
from core.services.application_service import ApplicationService
from core.services.invitation_service import InvitationService
from core.services.school_service import SchoolService

if TYPE_CHECKING:
    from core.database.crud.application_repo import ApplicationRepository
    from core.database.crud.invitation_repo import InvitationRepository
    from core.database.crud.user_repo import UserRepository


async def get_application_service(
    repo: Annotated["ApplicationRepository", Depends(get_application_repository)],
):
    yield ApplicationService(repo)


async def get_invitation_service(
    invitation_repo: Annotated[
        "InvitationRepository", Depends(get_invitation_repository)
    ],
    user_repo: Annotated["UserRepository", Depends(get_user_repository)],
):
    yield InvitationService(invitation_repo, user_repo)


async def get_school_service(
    school_repo: Annotated["SchoolRepository", Depends(get_school_repository)],
    subject_repo: Annotated["SubjectRepository", Depends(get_subject_repository)],
):
    yield SchoolService(school_repo, subject_repo)
