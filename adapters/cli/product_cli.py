import typer
from rich import print
from adapters.db.product_db import ProductDBPersistence

from application.product_service import ProductService
from application.product_interfaces import ProductInterface, ProductPersistenceInterface


app = typer.Typer(help="Product CLI management")


PERSISTENCES = {"sqlite": ProductDBPersistence()}


def persistence_validation(persistence: str):
    valid_persistences = PERSISTENCES.keys()
    if persistence not in valid_persistences:
        raise typer.BadParameter(
            f"Only the following persistences are implemented: {valid_persistences}"
        )

    return persistence


PERSISTENCE_OPTION = typer.Option(
    default="sqlite",
    help="The persistence used to save the product. "
    f"Valid values are {list(PERSISTENCES.keys())}",
    callback=persistence_validation,
)


@app.command()
def create(
    name: str = typer.Option(..., help="The product name"),
    price: float = typer.Option(..., help="The product price"),
    persistence: str = PERSISTENCE_OPTION,
) -> ProductInterface:
    """
    Create a product, using --name and --price arguments.
    Returns the product ID, Status, Name and Price.
    """
    persistence_class = _get_persistence(persistence)
    service = ProductService(persistence_class)

    product = service.create(name, price)
    print(
        "  [bold green]The product was successfully created![/bold green]\n"
        f"   [bold]Id:[/bold] {product.get_id()}\n"
        f"   [bold]Name:[/bold] {product.get_name()}\n"
        f"   [bold]Price:[/bold] {product.get_price()}\n"
        f"   [bold]Status:[/bold] {product.get_status()}"
    )


@app.command()
def get(
    id: str = typer.Option(..., help="The product ID"),
    persistence: str = PERSISTENCE_OPTION,
):
    """
    Get a product detail using it's ID
    Returns the product ID, Status, Name and Price.
    """
    persistence_class = _get_persistence(persistence)
    service = ProductService(persistence_class)

    product = service.get(id)
    print(product)


def _get_persistence(persistence: str) -> ProductPersistenceInterface:
    persistence_class = PERSISTENCES.get(persistence)
    if persistence_class is None:
        raise ValueError(f"Could not get persistence of type {persistence}")

    return persistence_class


if __name__ == "__main__":
    app()
