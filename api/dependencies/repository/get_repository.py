from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from api.dependencies.repository.get_validator import (
    get_application_validator,
    get_invitation_validator,
    get_school_validator,
)
from core.database.crud import (
    UserRepository,
    SchoolRepository,
    InvitationRepository,
    LessonRepository,
    ClassroomRepository,
)
from core.database.crud.application import ApplicationRepository
from core.database.crud.application import ApplicationValidator
from core.database.crud.base import BaseValidator
from core.database.crud.school import SchoolValidator
from core.database.crud.school_subject import SchoolSubjectRepository
from core.database.utils import db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


# SINGLETON


async def get_user_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield UserRepository(session)


async def get_school_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
    validator: Annotated["SchoolValidator", Depends(get_school_validator)],
):
    yield SchoolRepository(db=session, validator=validator)


async def get_application_repository(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
    validator: Annotated["ApplicationValidator", Depends(get_application_validator)],
):
    yield ApplicationRepository(db=session, validator=validator)


async def get_invitation_repository(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.session_getter),
    ],
    validator: Annotated["BaseValidator", Depends(get_invitation_validator)],
):
    yield InvitationRepository(db=session, validator=validator)


async def get_lesson_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield LessonRepository(db=session)


async def get_schedule_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
    validator: Annotated["SchoolValidator", Depends(get_school_validator)],
):
    yield SchoolRepository(db=session, validator=validator)


async def get_classroom_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield ClassroomRepository(db=session)


async def get_school_subject_repository(
    session: Annotated["AsyncSession", Depends(db_helper.session_getter)],
):
    yield SchoolSubjectRepository(db=session)
