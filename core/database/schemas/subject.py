from typing import Optional, List

from pydantic import BaseModel


class BaseSubject(BaseModel):
    subject_name: str


class CreateSubject(BaseSubject):
    description: Optional[str] = None


class ReadSubject(BaseSubject):
    pass


class CreateSubjects(BaseModel):
    subjects: List[CreateSubject]


class UpdateSubject(BaseModel):
    pass
