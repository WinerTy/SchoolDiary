from abc import ABC, abstractmethod

from core.types import Model


class BaseValidator(ABC):

    @abstractmethod
    def validate(self, instance: Model, **kwargs):
        """
        Базовый метод проверки
        :param instance: Объект проверки
        :param kwargs: Дополнительные аргументы
        :raises HTTPException: Вызов HTTP ошибки
        """
        pass

    @abstractmethod
    def validate_permisions(self, instance: Model, user_id: int):
        pass
