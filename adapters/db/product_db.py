from sqlmodel import SQLModel, Session, create_engine, select, Field

from application.product import Product
from application.product_service import PersistenceException
from application.product_interfaces import (
    ProductInterface,
    ProductPersistenceInterface,
)
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

ENGINES = {"sqlite": create_engine(url="sqlite://", echo=False)}


class ProductDB(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    status: str = "disabled"
    price: float


class ProductDBPersistence(ProductPersistenceInterface):
    @classmethod
    def get(cls, id: str, engine: str = "sqlite") -> ProductInterface:
        with Session(cls._get_engine(engine)) as session:
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

    @classmethod
    def save(
        cls, product: ProductInterface, engine: str = "sqlite"
    ) -> ProductInterface:
        with Session(cls._get_engine(engine)) as session:
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

    @staticmethod
    def _get_engine(engine: str):
        sql_engine = ENGINES.get(engine)
        if sql_engine is None:
            raise ValueError(
                f"The engine {engine} is invalid! Valid values are {ENGINES.keys()}"
            )

        SQLModel.metadata.create_all(sql_engine)

        return sql_engine
