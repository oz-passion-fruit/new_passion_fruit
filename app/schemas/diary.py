from pydantic import BaseModel
from datetime import datetime

class DiaryInSchema(BaseModel):
    title: str
    content: str

class DiaryOutSchema(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
