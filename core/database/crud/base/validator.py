from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.types import Model


class BaseValidator(ABC):
    @abstractmethod
    def validate(self, instance: "Model", **kwargs):
        pass
