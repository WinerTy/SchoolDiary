from typing import TypeVar

from core.database import BaseModel as SqlBase, BaseModel

Model = TypeVar("Model", bound=SqlBase)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
ReadSchema = TypeVar("ReadSchema", bound=BaseModel)
ResponseSchema = TypeVar("ResponseSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
