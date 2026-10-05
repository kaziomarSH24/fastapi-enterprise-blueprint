import email
from datetime import timedelta, datetime
from jose import jwt
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

load_dotenv()
# secret key from .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# Setup bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# make password Hash
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Hash password check funciton
def verify_password(plain_passowrd, hashed_password):
    return pwd_context.verify(plain_passowrd, hashed_password)


# Create token 
def create_access_token(data: dict):
    to_encode = data.copy()

    # token valid time (1h)
    expire = datetime.utcnow() + timedelta(minutes=60)

    to_encode.update({'exp': expire})

    #create token to use secret key
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# find token from request header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

# middleware function
def get_current_user_email(token: str = Depends(oauth2_scheme)):
    credentails_exception = HTTPException(
        status_code=401,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"}
    )

    try:
        #Decode using secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        email: str = payload.get('sub')

        if email is None:
            raise credentails_exception
        
        return email

    except JWTError:
        raise credentails_exception