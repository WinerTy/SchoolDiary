from datetime import date
from typing import List

from pydantic import BaseModel, computed_field

from .lesson import ReadLesson


class BaseSchedule(BaseModel):
    pass


class CreateSchedule(BaseSchedule):
    classroom_id: int
    schedule_date: date


class ReadSchedule(BaseSchedule):
    id: int
    lessons: List[ReadLesson]

    @computed_field
    @property
    def count_lessons(self) -> int:
        return len(self.lessons)

    class Config:
        from_attributes = True


class UpdateSchedule(BaseSchedule):
    pass
