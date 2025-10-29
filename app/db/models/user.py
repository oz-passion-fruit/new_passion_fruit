from tortoise import fields, models

# 기본적으로 모든 정보는 빈 값 허용하지 않음 주석을 넣어둔 내용은 빈값 허용
class User(models.Model):   # 사용자 모델
    id = fields.IntField(pk=True) # 사용자 고유 번호
    email = fields.CharField(max_length=255, unique=True) # 사용자 이메일 (로그인용)
    username = fields.CharField(max_length=255) # 사용자 이름
    hashed_password = fields.CharField(max_length=255) # 해싱된 비밀번호
    is_active = fields.BooleanField(default=True) # 활성화 상태
    created_at = fields.DatetimeField(auto_now_add=True) # 생성 시간
    updated_at = fields.DatetimeField(auto_now=True) # 수정 시간

    class Meta:
        table = "users"