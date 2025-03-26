from typing import List

from pydantic import BaseModel

from core.database.crud.user import UserRead


class BaseSchool(BaseModel):
    pass


class CreateSchool(BaseSchool):
    school_address: str
    school_description: str
    school_type: str
    school_phone: str
    school_name: str


class ReadSchool(BaseSchool):
    id: int
    director_id: int

    teachers: List[UserRead] = []


class UpdateSchool(BaseSchool):
    pass
