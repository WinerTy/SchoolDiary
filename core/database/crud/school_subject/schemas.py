from pydantic import BaseModel, constr


class SchoolSubjectBase(BaseModel):
    subject_name: constr(min_length=5, max_length=64)


class SchoolSubjectCreate(SchoolSubjectBase):
    school_id: int


class SchoolSubjectCreateRequest(SchoolSubjectBase):
    pass


class SchoolSubjectUpdate(SchoolSubjectBase):
    pass


class SchoolSubjectRead(SchoolSubjectBase):
    id: int
