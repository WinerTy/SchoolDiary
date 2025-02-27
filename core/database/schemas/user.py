from fastapi_users import schemas

from core.database.models.choices import ChoicesRole


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    first_name: str
    middle_name: str
    last_name: str


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    middle_name: str
    last_name: str


class UserUpdate(schemas.BaseUserUpdate):
    role: ChoicesRole
