from fastapi import FastAPI
from routers import products, users
from database.db import engine, Base
from models import product
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#create tables
# Base.metadata.create_all(bind=engine) # now it's handel by Alembic

#registare router
app.include_router(products.router)
app.include_router(users.router)


