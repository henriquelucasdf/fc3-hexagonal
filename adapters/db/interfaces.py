from abc import ABC, abstractmethod
from typing import Any


class EngineInterface(ABC):
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> Any:
        raise NotImplementedError
