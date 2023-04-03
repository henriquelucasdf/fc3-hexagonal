from abc import ABC, abstractmethod
from pydantic import BaseModel, UUID4


class ProductInterface(ABC, BaseModel):
    id: UUID4
    name: str
    status: str
    price: float

    @abstractmethod
    def enable(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def disable(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_price(self) -> float:
        raise NotImplementedError


class ProductServiceInterface(ABC):
    @abstractmethod
    def get(self, id: str) -> ProductInterface:
        raise NotImplementedError

    @abstractmethod
    def create(self, name: str, price: float) -> ProductInterface:
        raise NotImplementedError

    @abstractmethod
    def enable(self, product: ProductInterface) -> ProductInterface:
        raise NotImplementedError

    @abstractmethod
    def disable(self, product: ProductInterface) -> ProductInterface:
        raise NotImplementedError


class ProductReader(ABC):
    @classmethod
    @abstractmethod
    def get(cls, id: str) -> ProductInterface:
        raise NotImplementedError


class ProductWriter(ABC):
    @classmethod
    @abstractmethod
    def save(cls, product: ProductInterface) -> ProductInterface:
        raise NotImplementedError


class ProductPersistenceInterface(ProductReader, ProductWriter):
    pass
