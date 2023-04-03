from uuid import uuid4
from pydantic import UUID4, Field, confloat, constr
from typing import Union, Literal
from application.product_interfaces import ProductInterface


class ProductException(Exception):
    pass


class Product(ProductInterface):
    id: UUID4 = Field(default_factory=uuid4)
    name: constr(min_length=5)
    status: Union[Literal["enabled"], Literal["disabled"]] = "disabled"
    price: confloat(allow_inf_nan=False, ge=0.0)

    def enable(self) -> None:
        if self.price > 0:
            self.status = "enabled"

        else:
            raise ProductException(
                "The price must be greater than zero to enable the product"
            )

    def disable(self) -> None:
        if self.price == 0:
            self.status = "disabled"
        else:
            raise ProductException("The price must be zero to disable the product")

    def get_id(self) -> str:
        return self.id.__str__()

    def get_name(self) -> str:
        return self.name

    def get_status(self) -> str:
        return self.status

    def get_price(self) -> float:
        return self.price
