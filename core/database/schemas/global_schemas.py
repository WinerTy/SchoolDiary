from pydantic import BaseModel


class BaseResponse(BaseModel):
    detail: str
    status: int


class SuccessResponse(BaseResponse):
    pass
