
from core.database.crud.application import ApplicationValidator
from core.database.crud.invitation import InvitationValidator


async def get_application_validator() -> ApplicationValidator:
    yield ApplicationValidator()


async def get_invitation_validator() -> InvitationValidator:
    yield InvitationValidator()