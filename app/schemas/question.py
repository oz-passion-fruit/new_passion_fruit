from pydantic import BaseModel

# 질문 생성용 스키마
class QuestionCreateInSchema(BaseModel):
    question: str

# 질문 응답 스키마
class QuestionOutSchema(BaseModel):
    id: int
    question: str

    class Config:
        from_attributes = True
