import typer
from rich import print
from adapters.db.product_db import ProductDBPersistence, SQLiteLocalDatabase
from application.product_service import ProductService


app = typer.Typer(help="Product CLI management")


DATABASES = {
    "sqlite_local": ProductDBPersistence(db=SQLiteLocalDatabase())
}


def database_validation(database: str):
    valid_databases = DATABASES.keys()
    if database not in valid_databases:
        raise typer.BadParameter(
            f"Only the following persistences are implemented: {valid_databases}"
        )

    return database


DATABASE_OPTION = typer.Option(
    default="sqlite_local",
    help="The database used to save the product. "
    f"Valid values are {list(DATABASES.keys())}",
    callback=database_validation,
)

def _initialize_service(db_name: str) -> ProductService:
    database_class = DATABASES[db_name]
    return ProductService(persistence=database_class) 


@app.command()
def create(
    name: str = typer.Option(..., help="The product name"),
    price: float = typer.Option(..., help="The product price"),
    database: str = DATABASE_OPTION,
) -> None:
    """
    Create a product, using --name and --price arguments.
    Prints the product ID, Status, Name and Price.
    """
    service = _initialize_service(database)
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
    database: str = DATABASE_OPTION,
):
    """
    Get a product detail using it's ID
    Returns the product ID, Status, Name and Price.
    """
    service = _initialize_service(database)

    product = service.get(id)
    print(
        "  [bold green]The product was successfully obtained![/bold green]\n"
        f"   [bold]Id:[/bold] {product.get_id()}\n"
        f"   [bold]Name:[/bold] {product.get_name()}\n"
        f"   [bold]Price:[/bold] {product.get_price()}\n"
        f"   [bold]Status:[/bold] {product.get_status()}"
    )

@app.command()
def enable(
    id: str = typer.Option(..., help="The product ID"),
    database: str = DATABASE_OPTION,
):
    """
    Get a product detail using it's ID
    Returns the product ID, Status, Name and Price.
    """
    service = _initialize_service(database)

    product = service.get(id)
    service.enable(product)
    print(
        "  [bold green]The product was successfully enabled![/bold green]\n"
    )

@app.command()
def disable(
    id: str = typer.Option(..., help="The product ID"),
    database: str = DATABASE_OPTION,
):
    """
    Get a product detail using it's ID
    Returns the product ID, Status, Name and Price.
    """
    service = _initialize_service(database)

    product = service.get(id)
    service.disable(product)
    print(
        "  [bold green]The product was successfully disabled![/bold green]\n"
    )

if __name__ == "__main__":
    app()
