from fastapi import FastAPI
from routers import products
from database.db import engine, Base
from models import product

app = FastAPI()

#create tables
# Base.metadata.create_all(bind=engine) # now it's handel by Alembic

#registare router
app.include_router(products.router)


