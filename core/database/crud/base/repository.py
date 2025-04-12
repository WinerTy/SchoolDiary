from datetime import datetime
from typing import Generic, Type, Any, Optional, Union, Dict, List

from fastapi.exceptions import HTTPException
from sqlalchemy import select, inspect, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.types import Model, CreateSchema, ReadSchema, UpdateSchema


class BaseRepository(Generic[Model, CreateSchema, ReadSchema, UpdateSchema]):
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
        self,
        item_id: Any,
        error_message: Optional[str] = "Item not found",
        raise_ex: bool = True,
    ) -> Model:
        """
        Получает объект из базы данных по его идентификатору.

        Args:
            item_id: Идентификатор объекта (int, str или UUID в зависимости от модели).
            error_message: Сообщение об ошибке, которое будет возвращено, если объект не найден.
                По умолчанию: "Item not found".
            raise_ex: Флаг, указывающий нужно ли вызывать исключение если объект не найден.
                По умолчанию: True (исключение вызывается).

        Returns:
            Model: Найденный объект модели. Если объект не найден и raise_ex=False, возвращает None.

        Raises:
            HTTPException: Исключение с кодом 404, если объект не найден и raise_ex=True.
        """
        stmt = select(self.model).where(getattr(self.model, self.pk_field) == item_id)
        result = await self.db.execute(stmt)
        instance = result.scalars().first()
        if not instance and raise_ex:
            raise HTTPException(status_code=404, detail=error_message)
        return instance

    async def get_all(self) -> List[Model]:
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
        update_data: UpdateSchema,
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

    async def multiple_create(
        self,
        items: List[CreateSchema],
        integrity_error_message: str = "Item already exists",
    ) -> List[Model]:
        """
        Создает несколько объектов в базе данных.
        Args:
            items: Список объектов для создания.
            integrity_error_message: Сообщение об ошибке, которое будет возвращено, если объект уже существует.
                По умолчанию: "Item already exists".

        Returns:
            List[Model]: Список созданных объектов.

        Raises:
            HTTPException: Исключение с кодом 400, если объект уже существует.
            HTTPException: Исключение с кодом 500, если произошла Серверная ошибка.
        """
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
            raise HTTPException(status_code=400, detail=integrity_error_message)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def delete(self, item_id: Union[int, str]) -> None:
        try:
            stmt = delete(self.model).where(
                getattr(self.model, self.pk_field) == item_id
            )
            await self.db.execute(stmt)
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def get_with_filter(
        self,
        filter_fields: Dict[str, Union[str, int, float, datetime, None]],
        raise_ex: bool = True,
        error_message: Optional[str] = "Item not found",
        unique: bool = True,
    ) -> Union[Model, List[Model], None]:
        """
        Получает объекты из базы данных с фильтрацией по указанным полям.

        :param filter_fields: Словарь с полями и значениями для фильтрации
        :param raise_ex: Вызывать исключение, если объект не найден
        :param error_message: Сообщение об ошибке, если объект не найден
        :param unique: Применять ли unique() для результатов (нужно для JOIN запросов)
        :return: Один объект или список объектов, либо None
        """
        try:
            stmt = select(self.model)

            # Применяем все фильтры
            for field_name, field_value in filter_fields.items():
                if not hasattr(self.model, field_name):
                    raise AttributeError(
                        f"{self.model.__name__} has no attribute {field_name}"
                    )

                if field_value is not None:
                    stmt = stmt.where(getattr(self.model, field_name) == field_value)

            result = await self.db.execute(stmt)

            # Используем unique() если требуется и если есть JOIN-загрузки
            scalars = result.unique().scalars() if unique else result.scalars()

            instances = scalars.all()

            if not instances:
                if raise_ex:
                    raise HTTPException(status_code=404, detail=error_message)
                return None

            return instances[0] if len(instances) == 1 else instances

        except HTTPException:
            raise  # Пробрасываем HTTPException как есть
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
