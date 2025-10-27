from tortoise import fields, models
# 기본적으로 모든 정보는 빈 값 허용하지 않음 주석을 넣어둔 내용은 빈값 허용
class User(models.Model):   # 사용자 모델
    id = fields.IntField(pk=True) # 사용자 고유 번호        
    username = fields.CharField(max_length=255) # 사용자 이름
    password = fields.CharField(max_length=255) # 사용자 비밀번호

    class Meta:
        table = "users"