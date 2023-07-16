from abc import ABC, abstractmethod
from sqlalchemy.future import Engine


class DatabaseInterface(ABC):
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self) -> Engine:
        raise NotImplementedError
