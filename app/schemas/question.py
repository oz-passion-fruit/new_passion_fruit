from pydantic import BaseModel

class QuestionInSchema(BaseModel):
    question: str

class QuestionOutSchema(BaseModel):
    id: int
    question: str

    class Config:
        orm_mode = True
