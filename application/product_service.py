from pydantic import ValidationError
from application.product import Product
from application.product_interfaces import (
    ProductInterface,
    ProductPersistenceInterface,
    ProductServiceInterface,
)


class ProductServiceException(Exception):
    pass


class PersistenceException(Exception):
    pass


class ProductService(ProductServiceInterface):
    def __init__(self, persistence: ProductPersistenceInterface) -> None:
        self.persistence = persistence

    def get(self, id: str) -> ProductInterface:
        try:
            product = self.persistence.get(id)

        except PersistenceException as e:
            raise ProductServiceException(
                f"Could not get the product '{id}'. Error: {e}"
            ) from e

        return product

    def create(self, name: str, price: float) -> ProductInterface:
        try:
            product = Product(name=name, price=price)
            result = self.persistence.save(product=product)

        except ValidationError as e:
            raise ProductServiceException(
                f"An error occurred when trying to create the product: {e}"
            ) from e

        except PersistenceException as e:
            raise ProductServiceException(
                f"An error occurred when trying to save the product: {e}"
            ) from e

        return result

    def disable(self):
        pass

    def enable(self):
        pass
