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

#get product data
@router.get('/')
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return {"total": len(products), "data": products}
    
#get product by id
@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

#update product
@router.put("/{product_id}")
def update_product(product_id: int, product_data:ProductCreate, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price

    db.commit()
    db.refresh(product)

    return {
        "message": "Product update successfully!",
        "data": product
    }