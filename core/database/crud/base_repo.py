from typing import TypeVar, Generic, Type, Optional, Any

from pydantic import BaseModel
from sqlalchemy import select, inspect
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import BaseModel as SqlBase

Model = TypeVar("Model", bound=SqlBase)
CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
ReadSchema = TypeVar("ReadSchema", bound=BaseModel)
ResponseSchema = TypeVar("ResponseSchema", bound=BaseModel)


class BaseRepository(Generic[Model, CreateSchema, ReadSchema, ResponseSchema]):
    def __init__(
        self, model: Type[Model], db: AsyncSession, pk_field: str = "id"
    ) -> None:
        self.model: Type[Model] = model
        self.db: AsyncSession = db
        self.pk_field: str = pk_field

        mapper = inspect(model)
        if pk_field not in [col.name for col in mapper.primary_key]:
            raise AttributeError(
                f"Field '{pk_field}' is not a primary key in model {model.__name__}"
            )

    async def get_by_id(self, item_id: Any) -> Optional[Model]:
        result = await self.db.execute(
            select(self.model).where(getattr(self.model, self.pk_field) == item_id)
        )
        return result.scalars().one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Model]:
        result = await self.db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, item: CreateSchema) -> Model:
        try:
            db_item = self.model(**item.model_dump())
            self.db.add(db_item)
            await self.db.commit()
            return db_item
        except Exception as e:
            await self.db.rollback()
            raise e
