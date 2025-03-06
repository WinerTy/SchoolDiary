from typing import Optional

from pydantic import BaseModel


class BaseResponse(BaseModel):
    detail: str
    status: int


class SuccessResponse(BaseResponse):
    count_records: Optional[int] = None


class ErrorResponse(BaseResponse):
    pass
