from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(prefix="/products", tags=["products"])

#custom middleware
def verify_token(token: str):
    if token != 'secret123':
        raise HTTPException(status_code=401, detail="Unauthorized! Invalid Token.")
    return True



@router.get("/")
def get_products():
    return {"message": "Here is the product list!"}

#middleware validation route
@router.get("/vip-products", dependencies=[Depends(verify_token)])
def get_vip_products():
    return {"message": "Welcome VIP! Here are your exclusive products."}
