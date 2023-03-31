from application.product_interfaces import ProductInterface


class ProductException(Exception):
    pass


ENABLED = "enabled"
DISABLED = "disabled"


class Product(ProductInterface):
    def is_valid(self) -> bool:

        self._validate_types()

        if self.status not in [ENABLED, DISABLED]:
            raise ProductException(f"Status must be '{ENABLED}' or '{DISABLED}'")

        if self.price < 0:
            raise ProductException("Price must be greater or equal than zero.")

        if len(self.id) == 0:
            raise ProductException("Id must be defined")

        if len(self.name) == 0:
            raise ProductException("Name must be defined")

        return True

    def enable(self) -> None:
        if self.price > 0:
            self.status = ENABLED

        else:
            raise ProductException(
                "The price must be greater than zero to enable the product"
            )

    def disable(self) -> None:
        if self.price == 0:
            self.status = DISABLED
        else:
            raise ProductException("The price must be zero to disable the product")

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_status(self) -> str:
        return self.status

    def get_price(self) -> float:
        return self.price

    def _validate_types(self):

        types = {
            self.id: str,
            self.name: str,
            self.status: str,
            self.price: (float, int),
        }
        type_check = {key: isinstance(key, value) for key, value in types.items()}

        for key, value in type_check.items():
            if not value:
                if isinstance(types[key], tuple):
                    formatted_type = [item.__name__ for item in types[key]]
                else:
                    formatted_type = types[key].__name__
                raise ProductException(
                    f"The input '{key}' must be an '{formatted_type}'"
                )
