import typer
from adapters.db.product_db import ProductDBPersistence

from application.product_service import ProductService
from application.product_interfaces import ProductInterface

PERSISTENCES = {"sqlite": ProductDBPersistence()}

app = typer.Typer(help="Product CLI management")


def persistence_validation(persistence: str):
    valid_persistences = PERSISTENCES.keys()
    if persistence not in valid_persistences:
        raise typer.BadParameter(
            f"Only the following persistences are implemented: {valid_persistences}"
        )

    return persistence


@app.command(help="Create a Product")
def create(
    name: str = typer.Option(..., help="The product name"),
    price: float = typer.Option(..., help="The product price"),
    persistence: str = typer.Option(
        default="sqlite",
        help="The persistence used to save the product. "
        f"Valid values are {list(PERSISTENCES.keys())}",
        callback=persistence_validation,
    ),
) -> ProductInterface:
    persistence_class = PERSISTENCES.get(persistence)
    if persistence_class is None:
        raise ValueError("error")

    service = ProductService(persistence_class)

    product = service.create(name, price)
    print(
        "The product was successfully created!\n"
        f"   Id: {product.get_id()}\n   Name: {product.get_name()}\n"
        f"   Price: {product.get_price()}\n   Status: {product.get_status()}"
    )


@app.command(help="Delete a product")
def delete(id: str):
    print(f"deleted the id: {id}")


if __name__ == "__main__":
    app()
