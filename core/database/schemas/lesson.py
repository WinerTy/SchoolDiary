from datetime import time
from typing import Optional, List

from pydantic import BaseModel, field_validator

from core.database.schemas.subject import ReadSubject


class BaseLesson(BaseModel):
    subject_id: int


class CreateLesson(BaseLesson):
    schedule_id: int
    teacher_id: int
    start_time: time
    end_time: time
    additional_info: Optional[str] = None

    @field_validator("end_time")
    def validate_end_time(cls, end_time: time, values: dict):
        start_time = values.data.get("start_time")
        if start_time and end_time <= start_time:
            raise ValueError("end_time должен быть позже start_time")
        return end_time


class ReadLesson(BaseLesson):
    subject: ReadSubject
    start_time: time
    end_time: time

    @property
    def subject_name(self) -> str:
        return self.subject.subject_name

    class Config:
        from_attributes = True


class MultiCreateLessons(BaseModel):
    lessons: List[CreateLesson]

    @field_validator("lessons")
    def validate_lessons(cls, lessons: List[CreateLesson]):
        if len(lessons) > 8:
            raise ValueError("Максимум 8 уроков в день")
        for i in range(len(lessons)):
            for j in range(i + 1, len(lessons)):
                lesson1 = lessons[i]
                lesson2 = lessons[j]

                if not (
                    lesson1.end_time <= lesson2.start_time
                    or lesson2.end_time <= lesson1.start_time
                ):
                    raise ValueError(
                        f"Уроки {i} и {j} пересекаются по времени: "
                        f"{lesson1.start_time}-{lesson1.end_time} и "
                        f"{lesson2.start_time}-{lesson2.end_time}"
                    )
        return lessons


class UpdateLesson(CreateLesson):
    pass
