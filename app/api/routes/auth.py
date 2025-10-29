from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.schemas.user import UserCreateInSchema, UserOutSchema, Token, UserLoginInSchema
from app.db.models.user import User
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/auth", tags=["인증"])


@router.post("/signup", response_model=UserOutSchema, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreateInSchema):
    """
    회원가입
    - email: 이메일 (중복 불가)
    - username: 사용자 이름
    - password: 비밀번호
    """
    # 이메일 중복 체크
    existing_user = await User.filter(email=user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다."
        )
    
    # 사용자 생성
    hashed_password = get_password_hash(user_data.password)
    user = await User.create(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
    )
    
    return user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    로그인 (OAuth2 표준 형식)
    - username: 이메일 (OAuth2 표준에서는 username 필드 사용)
    - password: 비밀번호
    """
    # 이메일로 사용자 찾기 (OAuth2에서는 username 필드에 email을 넣음)
    user = await User.filter(email=form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Access Token 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/json", response_model=Token)
async def login_json(user_data: UserLoginInSchema):
    """
    로그인 (JSON 형식)
    - email: 이메일
    - password: 비밀번호
    """
    # 이메일로 사용자 찾기
    user = await User.filter(email=user_data.email).first()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Access Token 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOutSchema)
async def get_me(current_user: User = Depends(get_current_active_user)):
    """
    현재 로그인한 사용자 정보 조회
    """
    return current_user

