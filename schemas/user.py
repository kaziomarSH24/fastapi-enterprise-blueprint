from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


#for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#user responce to hide password
class UserResponse(BaseModel):
    id:int
    name:str
    email: EmailStr
    
    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    data: UserResponse