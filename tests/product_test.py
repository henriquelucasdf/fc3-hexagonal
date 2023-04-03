import uuid
import pytest
from application.product import Product, ProductException
from pydantic import ValidationError


def test_product_must_enable_only_if_price_is_positive():
    prod = Product(name="name1", price=10)
    prod.enable()

    assert prod.status == "enabled"


@pytest.mark.parametrize("price", [-1, -10.5, -10000])
def test_product_must_raise_an_error_if_price_is_not_positive(price):
    with pytest.raises(ValidationError):
        _ = Product(name="name1", price=price)


@pytest.mark.parametrize("price", [-1, -10.5, -10000])
def test_product_must_not_enable_if_price_is_negativa(price):
    prod = Product(name="name1", price=10)
    prod.price = price
    with pytest.raises(ProductException):
        prod.enable()

    assert prod.get_status() == "disabled"


def test_product_must_disable_only_if_price_is_zero():
    prod = Product(name="name1", price=0)
    prod.disable()

    assert prod.status == "disabled"


@pytest.mark.parametrize("price", [10.9, 7, 15, 100000])
def test_product_must_raise_an_error_if_price_is_not_zero(price):
    prod = Product(name="name1", status="enabled", price=price)
    with pytest.raises(ProductException):
        prod.disable()

    assert prod.status == "enabled"


def test_product_get_id_must_return_uuid_string():
    prod_id = uuid.uuid4()
    prod = Product(id=prod_id, name="name1", price=10)

    assert isinstance(prod.get_id(), str)
    assert prod_id.__str__() == prod.get_id()


def test_product_must_return_name():
    prod = Product(name="name123", price=10)

    assert isinstance(prod.get_name(), str)
    assert prod.get_name() == "name123"


def test_product_must_return_price():
    prod = Product(name="name123", price=10.567)

    assert isinstance(prod.get_price(), float)
    assert prod.get_price() == 10.567
