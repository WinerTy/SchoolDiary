from typing import Generic, Type, Optional, Any

from sqlalchemy import select, inspect
from sqlalchemy.ext.asyncio import AsyncSession

from core.types import Model, CreateSchema, ReadSchema, ResponseSchema


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

    async def create(self, item: CreateSchema, **kwargs) -> Model:
        try:
            data = item.model_dump()
            data.update(kwargs)

            db_item = self.model(**data)
            self.db.add(db_item)
            await self.db.commit()
            await self.db.refresh(db_item)
            return db_item
        except Exception as e:
            await self.db.rollback()
            raise e
