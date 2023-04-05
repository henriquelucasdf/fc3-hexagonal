import uuid
import pytest
from unittest.mock import MagicMock
from application.product import Product
from application.product_service import (
    PersistenceException,
    ProductService,
    ProductServiceException,
)

from pydantic import ValidationError, BaseModel
from pydantic.error_wrappers import ErrorWrapper


class MockModel(BaseModel):
    foo: str


def test_product_service_get_must_return_the_product_with_id():
    mock_id = uuid.uuid4()
    persistence = MagicMock()
    mock_product = Product(id=mock_id, name="mock_name", price=10)
    persistence.get = MagicMock(return_value=mock_product)

    service = ProductService(persistence)
    assert service.get(mock_id) == mock_product


def test_product_service_must_raise_exception_if_error_occur():
    mock_id = uuid.uuid4()
    persistence = MagicMock()
    persistence.get = MagicMock(side_effect=PersistenceException("an error"))

    service = ProductService(persistence)
    with pytest.raises(ProductServiceException):
        service.get(mock_id)

    persistence.get.assert_called_once_with(mock_id)


def test_product_service_create_must_return_the_product_with_id():
    persistence = MagicMock()
    mock_product = Product(name="mock_name", price=10)
    persistence.save = MagicMock(return_value=mock_product)

    service = ProductService(persistence)
    result = service.create(name="mock_name", price=10)
    assert result.get_name() == mock_product.get_name()
    assert result.get_price() == mock_product.get_price()


def test_product_service_must_raise_service_exception_if_pydantic_error_occur_creating():
    persistence = MagicMock()
    persistence.save = MagicMock(
        side_effect=ValidationError(
            errors=[ErrorWrapper(ValueError("foo"), loc=None)], model=MockModel
        )
    )

    err_message = "An error occurred when trying to create the product:"

    service = ProductService(persistence)
    with pytest.raises(ProductServiceException) as err:
        service.create(name="mock_name", price=10)

    persistence.save.assert_called_once()
    assert err_message in err.exconly(True)


def test_product_service_must_raise_service_exception_if_persistence_error_occur_creating():
    persistence = MagicMock()
    persistence.save = MagicMock(side_effect=PersistenceException("error"))

    err_message = "An error occurred when trying to save the product:"

    service = ProductService(persistence)
    with pytest.raises(ProductServiceException) as err:
        service.create(name="mock_name", price=10)

    persistence.save.assert_called_once()
    assert err_message in err.exconly(True)
