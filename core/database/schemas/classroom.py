from pydantic import BaseModel


class BaseClassroom(BaseModel):
    pass


class CreateClassroom(BaseClassroom):
    pass


class ReadClassroom(BaseClassroom):
    id: int
