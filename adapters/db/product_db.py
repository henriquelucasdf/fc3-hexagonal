from sqlmodel import SQLModel, Session, create_engine, select, Field
from adapters.db.interfaces import DatabaseInterface
from sqlalchemy.future import Engine
from application.product import Product
from application.product_service import PersistenceException
from application.product_interfaces import (
    ProductInterface,
    ProductPersistenceInterface,
)
from sqlalchemy.exc import NoResultFound, MultipleResultsFound


class SQLiteLocalDatabase(DatabaseInterface):
    def __init__(self) -> None:
        self._engine = create_engine(url="sqlite:///sqlite.db", echo=False)
        SQLModel.metadata.create_all(self._engine)

    def get(self) -> Engine:
        return self._engine


class ProductDB(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    status: str = "disabled"
    price: float


class ProductDBPersistence(ProductPersistenceInterface):
    def __init__(self, db: DatabaseInterface) -> None:
        self.db = db

    def get(self, id: str) -> ProductInterface:
        with Session(self.db.get()) as session:
            statement = select(ProductDB).where(ProductDB.id == id)

            try:
                product_query = session.exec(statement).one()

            except NoResultFound:
                raise PersistenceException(f"No products were found with the id '{id}'")

            except MultipleResultsFound:
                raise PersistenceException(
                    f"Multiple products were found for the id '{id}'"
                )

            except Exception as e:
                raise PersistenceException(f"An error occurred getting the data: {e}")

        return Product(**product_query.dict())

    def save(self, product: ProductInterface) -> ProductInterface:
        with Session(self.db.get()) as session:
            db_product = session.get(ProductDB, product.id)

            if db_product is None:
                new_product_db = ProductDB(**product.dict())
                session.add(new_product_db)
                session.commit()

            else:
                for key, value in product.dict().items():
                    setattr(db_product, key, value)

                session.add(db_product)
                session.commit()
                session.refresh(db_product)

        return product
