from core.database.crud.application import ApplicationValidator
from core.database.crud.invitation import InvitationValidator
from core.database.crud.school import SchoolValidator


async def get_application_validator() -> ApplicationValidator:
    yield ApplicationValidator()


async def get_invitation_validator() -> InvitationValidator:
    yield InvitationValidator()


async def get_school_validator() -> SchoolValidator:
    yield SchoolValidator()
