from typing import Optional

from pydantic import BaseModel


class BaseResponse(BaseModel):
    detail: str
    status: int
    count_records: Optional[int] = None


class SuccessResponse(BaseResponse):
    pass
