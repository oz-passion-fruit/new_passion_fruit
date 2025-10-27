from pydantic import BaseModel

class UserInSchema(BaseModel):
    username: str
    password: str

class UserOutSchema(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
