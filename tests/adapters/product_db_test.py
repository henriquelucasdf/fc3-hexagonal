import pytest
from sqlmodel import Session, SQLModel
from sqlalchemy.exc import NoResultFound

from application.product import Product
from application.product_service import PersistenceException, ProductService
from adapters.db.product_db import ProductDB, ProductDBPersistence, SQLiteLocalDatabase

db = SQLiteLocalDatabase()


class TestProductDBPersistence:
    def setup_class(self):
        SQLModel.metadata.create_all(db.get())

        self.session = Session(db.get())
        self.valid_product_1 = Product(
            name="valid_product_1", status="enabled", price=123
        )
        self.valid_product_2 = Product(
            name="valid_product_2", status="disabled", price=0
        )

        # add products to DB
        self.session.add(ProductDB(**self.valid_product_1.dict()))
        self.session.add(ProductDB(**self.valid_product_2.dict()))
        self.session.commit()

    def teardown_class(self):
        SQLModel.metadata.drop_all(db.get())
        self.session.close()

    def test_get_must_return_product(self):
        product_db = ProductDBPersistence(db).get(self.valid_product_1.id)
        assert product_db == self.valid_product_1

    def test_get_must_raise_error_if_no_product_is_found(self):
        with pytest.raises(
            expected_exception=PersistenceException,
            match="No products were found with the id 'abcde'",
        ):
            ProductDBPersistence(db).get(id="abcde")

    def test_save_must_add_new_product(self):
        new_product = Product(name="new_product", status="enabled", price=20)
        returned_product = ProductDBPersistence(db).save(new_product)

        product_query = ProductDBPersistence(db).get(new_product.id)
        assert product_query == new_product == returned_product

    def test_save_must_update_existing_product(self):
        updated_product = self.valid_product_1.copy()
        updated_product.name = "updated_product"
        updated_product.price = 12345

        returned_product = ProductDBPersistence(db).save(updated_product)
        product_query = ProductDBPersistence(db).get(updated_product.id)
        assert product_query == updated_product == returned_product

    def test_service_interaction_with_persistence(self):
        persistence = ProductDBPersistence(db)
        service = ProductService(persistence)
        product_created = service.create(name="test-using-service", price=25)

        product_saved = service.get(product_created.get_id())
        assert product_created == product_saved
