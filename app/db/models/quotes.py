from tortoise import fields, models

class Quote(models.Model): # 명언 스크래핑에 사용 될 모델
    id = fields.IntField(pk=True) # 명언 고유 번호
    content = fields.TextField() # 명언 내용
    author = fields.CharField(max_length=255, null=True) # 명언 작가 , 작가 미상의 경우도 있을 것 같아 빈 값 허용했습니다.

    class Meta:
        table = "quotes"