from uuid import uuid4
from abc import ABC, abstractmethod


class ProductInterface(ABC):
    def __init__(
        self,
        name: str,
        id: str = str(uuid4()),
        status: str = "disabled",
        price: float = 0,
    ) -> None:
        self.id = id
        self.name = name
        self.status = status
        self.price = price

    @abstractmethod
    def is_valid(self) -> bool:
        raise NotImplementedError

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
