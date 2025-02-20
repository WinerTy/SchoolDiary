from typing import Optional, List

from pydantic import BaseModel


class BaseSubject(BaseModel):
    subject_name: str


class CreateSubject(BaseSubject):
    description: Optional[str] = None


class ReadSubject(BaseSubject):
    id: int


class CreateSubjects(BaseModel):
    subjects: List[CreateSubject]
