from core.database.crud.application import ApplicationValidator


async def get_application_validator() -> ApplicationValidator:
    yield ApplicationValidator()
