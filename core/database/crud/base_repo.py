from typing import Generic, Type, Any, Optional

from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, inspect
from sqlalchemy.exc import IntegrityError
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

    async def get_by_id(
        self, item_id: Any, error_message: Optional[str] = "Item not found"
    ) -> Model:
        stmt = select(self.model).where(getattr(self.model, self.pk_field) == item_id)
        result = await self.db.execute(stmt)
        instance = result.scalars().first()
        if not instance:
            raise HTTPException(status_code=404, detail=error_message)
        return instance

    async def get_all(self) -> list[Model]:
        result = await self.db.execute(select(self.model))
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
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Item already exists")
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def update(
        self,
        item_id: Any,
        update_data: BaseModel,  # Только Pydantic схема
    ) -> Model:
        """
        Обновляет объект в базе данных.
        :param item_id: Идентификатор объекта.
        :param update_data: Данные для обновления (только Pydantic схема).
        :return: Обновленный объект.
        """
        try:
            # Получаем объект из базы данных
            instance = await self.get_by_id(item_id)

            # Преобразуем Pydantic схему в словарь, исключая неустановленные поля
            update_dict = update_data.model_dump(exclude_unset=True)

            # Обновляем поля объекта
            for key, value in update_dict.items():
                setattr(instance, key, value)

            # Сохраняем изменения в базе данных
            self.db.add(instance)
            await self.db.commit()
            await self.db.refresh(instance)

            return instance
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def multiple_create(self, items: list[CreateSchema]) -> list[Model]:
        if not items:
            raise HTTPException(status_code=400, detail="No items provided")
        try:
            db_items = [self.model(**item.model_dump()) for item in items]
            self.db.add_all(db_items)
            await self.db.commit()
            for item in db_items:
                await self.db.refresh(item)
            return db_items
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail="Item already exists")
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
