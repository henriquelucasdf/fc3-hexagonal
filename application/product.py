from abc import ABC, abstractmethod


class ProductException(Exception):
    pass


class ProductInterface(ABC):
    def __init__(self, id: str, name: str, status: str, price: float) -> None:
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


class Product(ProductInterface):
    def is_valid(self) -> bool:
        raise NotImplementedError

    def enable(self) -> None:
        raise NotImplementedError

    def disable(self) -> None:
        raise NotImplementedError

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_status(self) -> str:
        return self.status

    def get_price(self) -> float:
        return self.price
