from typing import TypeVar

from pydantic import BaseModel

from core.database import BaseModel as SqlBase

Model = TypeVar("Model", bound=SqlBase)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
ReadSchema = TypeVar("ReadSchema", bound=BaseModel)
ResponseSchema = TypeVar("ResponseSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
