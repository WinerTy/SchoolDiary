from typing import Optional, Annotated

from pydantic import BaseModel, Field


class GradeBase(BaseModel):
    additional_info: Annotated[Optional[str], Field(max_length=256)] = None


class GradeCreateRequest(GradeBase):
    user_id: int
    lesson_id: int
    grade: int = Field(ge=1, le=5)


class GradeCreate(GradeBase):
    user_id: int
    lesson_id: int
    grade: int = Field(ge=1, le=5)


class GradeRead(GradeBase):
    id: int
    grade: int
