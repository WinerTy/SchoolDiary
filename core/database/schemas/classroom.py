from typing import TYPE_CHECKING, List

from pydantic import BaseModel, computed_field

if TYPE_CHECKING:
    from core.database.crud.user import UserRead


class BaseClassroom(BaseModel):
    pass


class CreateClassroom(BaseClassroom):
    pass


class ReadClassroom(BaseClassroom):
    id: int
    students: List["UserRead"]

    @computed_field
    @property
    def count_of_schedules(self) -> int:
        return len(self.students)


class UpdateClassroom(BaseClassroom):
    pass
