from tortoise import fields, models

class Question(models.Model): # 질문 모델 
    id = fields.IntField(pk=True) # 질문 고유 번호
    question = fields.TextField() # 질문 내용
    # 질문의 경우는 작가 미상인 경우도 있을 것 같아 작가 부분을 만들지 않았습니다.
    
    class Meta:
        table = "questions"
