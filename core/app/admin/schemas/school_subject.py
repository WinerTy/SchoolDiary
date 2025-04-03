from pydantic import BaseModel, field_validator


class SchoolSubjectSchema(BaseModel):
    subject_name: str

    @field_validator("subject_name")
    def validate_subject_name(cls, subject_name: str):
        if " " in subject_name:
            raise ValueError("Название предмета не должен содержать пробелы")
        return subject_name
