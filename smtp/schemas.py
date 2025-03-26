from typing import List, Dict, Any

from pydantic import EmailStr, BaseModel


class EmailSchema(BaseModel):
    email: List[EmailStr]
    body: Dict[str, Any] = None


class ContentSchema(BaseModel):
    content: Dict[str, Any]
