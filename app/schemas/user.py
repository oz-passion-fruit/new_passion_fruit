from pydantic import BaseModel, EmailStr
from typing import Optional

# JWT 토큰 스키마
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None

# 회원가입용 스키마
class UserCreateInSchema(BaseModel):
    email: EmailStr
    username: str
    password: str

# 로그인용 스키마
class UserLoginInSchema(BaseModel):
    email: EmailStr
    password: str

# 응답용 스키마
class UserOutSchema(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool

    class Config:
        from_attributes = True

