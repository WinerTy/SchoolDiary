from pydantic import BaseModel


class BaseSchool(BaseModel):
    pass


class CreateSchool(BaseSchool):
    school_address: str
    school_description: str
    school_type: str
    school_phone: str


class ReadSchool(BaseSchool):
    id: int
    director_id: int
