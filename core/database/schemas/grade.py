from pydantic import BaseModel

from core.database.schemas.lesson import ReadLesson


class BaseGrade(BaseModel):
    id: int
    grade: int


class CreateGrade(BaseModel):
    additional_info: str


class UpdateGrade(BaseModel):
    grade: int


class ReadGrade(BaseGrade):
    lesson: ReadLesson
    additional_info: str
