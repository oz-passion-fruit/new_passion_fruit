from pydantic import BaseModel, EmailStr
from typing import Optional
class Token(BaseModel):
    access_token: str
    token_type: str
class TokenData(BaseModel):
    email: Optional[EmailStr] = None
class UserBase(BaseModel):
    email: EmailStr
class UserCreate(UserBase):
    password: str
class UserLogin(BaseModel):
    email: EmailStr
    password: str
class User(UserBase):
    id: int
    is_active: bool
    class Config:
        from_attributes = True