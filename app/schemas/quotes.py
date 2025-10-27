from pydantic import BaseModel
from typing import Optional

class QuoteInSchema(BaseModel):
    content: str
    author: Optional[str] = None

class QuoteOutSchema(BaseModel):
    id: int
    content: str
    author: Optional[str] = None

    class Config:
        orm_mode = True
