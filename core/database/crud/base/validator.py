from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from core.types import Model


class BaseValidator(ABC):
    @abstractmethod
    def validate(
        self,
        instance: "Model",
        action: Literal["create", "read", "update", "delete"],
        **kwargs
    ):
        pass
