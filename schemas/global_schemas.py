from pydantic import BaseModel


class NotFoundResponse(BaseModel):
    detail: str


class ForbiddenResponse(BaseModel):
    detail: str
