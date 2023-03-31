import pytest
from application.product import Product, ProductException


def test_product_must_enable_only_if_price_is_positive():
    prod = Product("name", "id123", "disabled", 10)
    prod.enable()

    assert prod.status == "enabled"


@pytest.mark.parametrize("price", [0, -1, -10.5])
def test_product_must_raise_an_error_if_price_is_not_positive(price):
    prod = Product("name", "id123", "disabled", price)
    with pytest.raises(ProductException):
        prod.enable()

    assert prod.status == "disabled"


def test_product_must_disable_only_if_price_is_zero():
    prod = Product("name", "id123", "enabled", 0)
    prod.disable()

    assert prod.status == "disabled"


@pytest.mark.parametrize("price", [10.9, 7, -1, -10.5])
def test_product_must_raise_an_error_if_price_is_not_zero(price):
    prod = Product("name", "id123", "enabled", price)
    with pytest.raises(ProductException):
        prod.disable()

    assert prod.status == "enabled"


def test_product_must_be_validated():
    prod = Product("name", "id123")
    prod.is_valid()


@pytest.mark.parametrize(
    "name, id, status, price",
    [
        ("", "asdf", "disabled", 0),
        ("123", "", "disabled", 0),
        ("123", "asdf", "not_enabled", 0),
        ("123", "", "enabled", "0"),
        (123, "id", "enabled", 0.5),
        ("", "id", "enabled", 0.5),
        ("123", "", "enabled", 0.5),
        ("123", "id", "enabled", -5.5),
    ],
)
def test_product_validation_must_raise(id, name, status, price):
    prod = Product(name, id, status, price)
    with pytest.raises(ProductException):
        prod.is_valid()
