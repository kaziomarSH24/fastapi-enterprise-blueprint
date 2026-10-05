from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from models.product import Product
from schemas.product import ProductCreate


router = APIRouter(prefix="/products", tags=["Products API"])

#post route for save data to database
@router.post("/")
def create_product(product_data: ProductCreate, db: Session = Depends(get_db) ):
    #create Product instance
    new_product = Product(
        name=product_data.name,
        description=product_data.description,
        price= product_data.price
    )

    #data save to database
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return {'message': 'Product created successfully!', 'data': new_product}