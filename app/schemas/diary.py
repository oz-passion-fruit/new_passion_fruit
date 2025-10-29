from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 일기 생성용 스키마
class DiaryCreateInSchema(BaseModel):
    title: str
    content: str

# 일기 수정용 스키마
class DiaryUpdateInSchema(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# 일기 응답 스키마
class DiaryOutSchema(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


