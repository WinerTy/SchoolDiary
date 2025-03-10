from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator, Field


class BaseApplication(BaseModel):
    director_full_name: str
    school_name: str = Field(min_length=6, max_length=64)

    @field_validator("director_full_name")
    def validate_director_full_name(cls, director_full_name: str):
        words = director_full_name.split(" ")
        if len(words) < 3:
            raise ValueError("Укажите полное Имя, Фамилию и Отчество")
        return director_full_name


class CreateApplication(BaseApplication):
    director_phone: str
    director_email: EmailStr

    school_address: str
    school_phone: str
    school_description: str
    school_type: Optional[str] = None


class ReadApplication(BaseApplication):
    id: int
    status: str


class UpdateApplication(CreateApplication):
    pass
