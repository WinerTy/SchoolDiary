from datetime import date
from typing import TYPE_CHECKING, List, Tuple, Optional, Union

from fastapi import Request
from jinja2 import Template
from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import BaseModel
from core.database.mixins import PkIntMixin
from .lesson import Lesson

if TYPE_CHECKING:
    from .classroom import Classroom


class Schedule(BaseModel, PkIntMixin):
    __tablename__ = "schedules"

    classroom_id: Mapped[int] = mapped_column(
        ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False
    )

    lessons: Mapped[List["Lesson"]] = relationship(
        "Lesson", back_populates="schedule", order_by="Lesson.start_time", lazy="joined"
    )

    schedule_date: Mapped[date] = mapped_column(Date, nullable=False)

    classroom: Mapped["Classroom"] = relationship(
        "Classroom", back_populates="schedules", lazy="joined"
    )

    def __str__(self) -> str:
        return f"{self.classroom} - {self.schedule_date}"

    def convert_date(self, date_format: str = "%d.%m.%Y") -> str:
        return self.schedule_date.strftime(date_format)

    def count_lessons(self) -> int:
        return len(self.lessons)

    def validate_lessons(
        self,
        new_lessons: Union["Lesson", List["Lesson"]],
        existing_lessons: Optional[List["Lesson"]] = None,
    ) -> Tuple[bool, Optional["Lesson"]]:
        lessons_to_check = (
            [new_lessons] if isinstance(new_lessons, Lesson) else new_lessons
        )
        existing = existing_lessons if existing_lessons is not None else self.lessons

        for i, lesson1 in enumerate(lessons_to_check):
            for lesson2 in lessons_to_check[i + 1 :]:
                if self._check_time_overlap(lesson1, lesson2):
                    return False, lesson2

        for new_lesson in lessons_to_check:
            for existing_lesson in existing:
                if existing_lesson.id == new_lesson.id:
                    continue

                if self._check_time_overlap(new_lesson, existing_lesson):
                    return False, existing_lesson

        return True, None

    @staticmethod
    def _check_time_overlap(lesson1: "Lesson", lesson2: "Lesson") -> bool:
        return (
            lesson1.start_time < lesson2.end_time
            and lesson1.end_time > lesson2.start_time
        )

    def validate_new_lesson(
        self, new_lesson: "Lesson"
    ) -> Tuple[bool, Optional["Lesson"]]:
        """
        Проверяет, есть ли конфликты у нового урока с существующими.

        Возвращает:
            Tuple[bool, Optional[Lesson]]:
                - bool: True если валидация прошла, False если есть конфликты
                - Lesson: ссылка на конфликтующий урок (если есть)
        """
        for lesson in self.lessons:
            if lesson.id == new_lesson.id:
                continue

            if (
                new_lesson.start_time < lesson.end_time
                and new_lesson.end_time > lesson.start_time
            ):
                return False, lesson  # Найден конфликт

        return True, None  # Конфликтов нет

    async def __admin_repr__(self, request: Request) -> str:
        return f"Расписание {self.classroom} - {self.convert_date()}"

    async def __admin_select2_repr__(self, request: Request) -> str:
        template = Template(
            """<span>{{ data }}</span>""",
            autoescape=True,
        )
        return template.render(data=self.convert_date())
