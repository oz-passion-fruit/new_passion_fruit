from pydantic import BaseModel
from typing import Optional

# 명언 생성용 스키마
class QuoteCreateInSchema(BaseModel):
    content: str
    author: Optional[str] = None

# 명언 응답 스키마
class QuoteOutSchema(BaseModel):
    id: int
    content: str
    author: Optional[str] = None

    class Config:
        from_attributes = True
