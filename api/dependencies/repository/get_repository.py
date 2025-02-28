from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from core.database.crud import (
    UserRepository,
    SchoolRepository,
    ApplicationRepository,
    InvitationRepository,
    SubjectRepository,
    LessonRepository,
    ScheduleRepository,
    ClassroomRepository,
)
from core.database.utils import db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield UserRepository(session)


async def get_school_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield SchoolRepository(db=session)


async def get_application_repository(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    yield ApplicationRepository(db=session)


async def get_invitation_repository(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
):
    yield InvitationRepository(db=session)


async def get_subject_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield SubjectRepository(db=session)


async def get_lesson_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield LessonRepository(db=session)


async def get_schedule_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield SchoolRepository(db=session)


async def get_schedule_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield ScheduleRepository(db=session)


async def get_classroom_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield ClassroomRepository(db=session)
