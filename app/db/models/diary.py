from tortoise import fields, models

class diary(models.Model): # 일기 모델
    id = fields.IntField(pk=True) # 일기 고유 번호
    title = fields.CharField(max_length=255) # 일기 제목
    content = fields.TextField() # 일기 내용
    created_at = fields.DatetimeField(auto_now_add=True) # 일기 생성 시간
    updated_at = fields.DatetimeField(auto_now=True) # 일기 수정 시간

    class Meta:
        table = "diaries"