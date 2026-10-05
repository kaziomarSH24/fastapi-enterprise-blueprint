from fastapi import FastAPI
from routers import products
from database.db import engine, Base
from models import Product

app = FastAPI()

#create tables
Base.metadata.create_all(bind=engine)

#registare router
app.include_router(products.router)


