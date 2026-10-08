from fastapi.security import OAuth2PasswordRequestForm
from fastapi.openapi.models import OAuth2
from core.security import create_access_token, verify_password
from schemas.user import UserLogin, LoginResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.db import get_db
from models.user import User
from schemas.user import UserCreate, UserResponse
from core.security import get_password_hash, get_current_user

router = APIRouter(prefix="/users", tags=["Users API"])


# User registation
@router.post("/register")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):

    #check email is already exist or not
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code = 400, detail="Email already registered!")
    
    # Hash password
    hashed_pass = get_password_hash(user_data.password)

    # create object for save user to database
    new_user = User(
        name = user_data.name,
        email = user_data.email,
        password = hashed_pass
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{
        "message": "User created Successfully!",
        'data': new_user
    }


#user login
@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == user_credentials.username).first()

    #check user
    if not user:
        raise HTTPException(status_code= 401, detail = "Invalid Credentials")
    
    #verify password
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code= 401, detail = "Invalid Credentials")
    
    #generate token if verify the password is valid
    access_token = create_access_token(data = {'sub':user.email})

    #return token 
    return {
        'access_token': access_token,
        'token_type': 'bearer'
        # 'data': user
    }


# Protected Route
# @router.get('/me', response_model=UserResponse)
# def get_profile(db: Session = Depends(get_db), email: str = Depends(get_current_user_email)):
#     # find user from data base to get email from middleware
#     user = db.query(User).filter(User.email == email).first()

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     return user

@router.get('/me', response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user