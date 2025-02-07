from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseApplication(BaseModel):
    director_full_name: str
    school_name: str


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
