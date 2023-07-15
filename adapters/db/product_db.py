from sqlmodel import SQLModel, Session, create_engine, select, Field
from adapters.db.interfaces import EngineInterface
from sqlalchemy.future import Engine
from application.product import Product
from application.product_service import PersistenceException
from application.product_interfaces import (
    ProductInterface,
    ProductPersistenceInterface,
)
from sqlalchemy.exc import NoResultFound, MultipleResultsFound


class SQLiteEngine(EngineInterface):
    def __init__(self) -> None:
        self._engine = create_engine(url="sqlite://", echo=False)
    
    def get(self) -> Engine:
        return self._engine


class ProductDB(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    status: str = "disabled"
    price: float


class ProductDBPersistence(ProductPersistenceInterface):
    @classmethod
    def get(cls, id: str, engine: EngineInterface) -> ProductInterface:
        with Session(engine.get()) as session:
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
        with Session(engine.get()) as session:
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
