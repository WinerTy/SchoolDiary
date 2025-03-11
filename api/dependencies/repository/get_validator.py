


from core.database.crud import ApplicationValidator, BaseValidator

async def get_application_repository() -> BaseValidator:
    yield ApplicationValidator()