from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, field_validator

from core.database.models.choices import ChoicesRole


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    first_name: str
    middle_name: str
    last_name: str
    role: ChoicesRole


class UserUpdateRequest(schemas.BaseUserUpdate):
    pass


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    middle_name: str
    last_name: str


class UserUpdate(schemas.BaseUserUpdate):
    role: Optional[ChoicesRole] = None

    @field_validator("password")
    def validate_password(cls, password: str):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return password


class UserLogin(BaseModel):
    username: str
    password: str
