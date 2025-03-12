from typing import Annotated, TYPE_CHECKING

from fastapi.params import Depends

from api.dependencies.repository import (
    get_application_repository,
    get_user_repository,
    get_invitation_repository,
    get_school_repository,
    get_subject_repository,
    get_lesson_repository,
    get_schedule_repository,
    get_classroom_repository,
)
from core.services import (
    ApplicationService,
    InvitationService,
    LessonService,
    SchoolService,
)

if TYPE_CHECKING:
    from core.database.crud.application import ApplicationRepository
    from core.database.crud.invitation import InvitationRepository
    from core.database.crud.user import UserRepository
    from core.database.crud import (
        LessonRepository,
        ScheduleRepository,
        ClassroomRepository,
    )


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
    lesson_repo: Annotated["LessonRepository", Depends(get_lesson_repository)],
    schedule_repo: Annotated["ScheduleRepository", Depends(get_schedule_repository)],
    classroom_repo: Annotated["ClassroomRepository", Depends(get_classroom_repository)],
):
    yield SchoolService(
        school_repo, subject_repo, lesson_repo, schedule_repo, classroom_repo
    )


async def get_lesson_service(
    lesson_repo: Annotated["LessonRepository", Depends(get_lesson_repository)],
):
    yield LessonService(lesson_repo)
