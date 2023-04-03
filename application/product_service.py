from application.product_interfaces import (
    ProductInterface,
    ProductPersistenceInterface,
    ProductServiceInterface,
)


class ProductServiceException(Exception):
    pass


class ProductService(ProductServiceInterface):
    def __init__(self, persistence: ProductPersistenceInterface) -> None:
        self.persistence = persistence

    def get(self, id: str) -> ProductInterface:
        try:
            product = self.persistence.get(id)

        except Exception as e:
            raise ProductServiceException(
                f"Could not get the product '{id}'. Error: {e}"
            ) from e

        return product
