from contextlib import asynccontextmanager
from fastapi import FastAPI, status, HTTPException
from adapters.db.product_db import ProductDBPersistence, SQLiteLocalDatabase
from application.product_service import ProductService, ProductServiceException

services = {}

@asynccontextmanager
async def initialize_service(app: FastAPI):
    database = ProductDBPersistence(db=SQLiteLocalDatabase())
    services["local"] = ProductService(database)
    yield
    services.clear()


app = FastAPI(debug=True, lifespan=initialize_service)


@app.get("/")
def root():
    return {"message": "webserver is live"}

@app.get("/healthcheck", status_code=status.HTTP_200_OK)
async def health():
    return {'healthcheck': 'Everything OK!'}


@app.get("/product/get")
async def get(id: str):
    try:
        product = services["local"].get(id)
    except ProductServiceException as e:
        raise HTTPException(404, f"Product with ID '{id}' was not found") from e
    
    return {
        "product": {
            "id": product.get_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "status": product.get_status()
        }
    }


@app.get("/product/create")
async def create(name: str, price: float):
    try:
        product = services["local"].create(name, price)
    except ProductServiceException as e:
        raise HTTPException(500, f"Could not create product: {e}") from e
    return {
        "product": {
            "id": product.get_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "status": product.get_status()
        }
    }

@app.get("/product/enable")
async def enable(id: str):
    try:
        product = services["local"].get(id)
    except ProductServiceException as e:
        raise HTTPException(404, f"Product with ID '{id}' was not found") from e

    try:
        new_product = services["local"].enable(product)
    except ProductServiceException as e:
        raise HTTPException(500, f"Could not enable product: {e}") from e
    return {
        "product": {
            "id": new_product.get_id(),
            "name": new_product.get_name(),
            "price": new_product.get_price(),
            "status": new_product.get_status()
        }
    }


@app.get("/product/disable")
async def disable(id: str):
    try:
        product = services["local"].get(id)
    except ProductServiceException as e:
        raise HTTPException(404, f"Product with ID '{id}' was not found") from e

    try:
        new_product = services["local"].disable(product)
    except ProductServiceException as e:
        raise HTTPException(500, f"Could not disable product: {e}") from e
    return {
        "product": {
            "id": new_product.get_id(),
            "name": new_product.get_name(),
            "price": new_product.get_price(),
            "status": new_product.get_status()
        }
    }
