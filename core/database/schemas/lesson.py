from datetime import time
from typing import Optional, List

from pydantic import BaseModel


class BaseLesson(BaseModel):
    subject_id: int


class CreateLesson(BaseLesson):
    schedule_id: int
    teacher_id: int
    start_time: time
    end_time: time
    additional_info: Optional[str] = None


class ReadLesson(BaseLesson):
    id: int


class MultiCreateLessons(BaseModel):
    lessons: List[CreateLesson]
