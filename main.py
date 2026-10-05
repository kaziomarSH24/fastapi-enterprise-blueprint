from fastapi import FastAPI
from routers import products


app = FastAPI()

#registare router
app.include_router(products.router)


