from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from app.schemas.diary import DiaryCreateInSchema, DiaryUpdateInSchema, DiaryOutSchema
from app.db.models.diary import Diary
from app.db.models.user import User
from app.core.security import get_current_active_user

router = APIRouter(prefix="/diaries", tags=["일기"])


@router.post("", response_model=DiaryOutSchema, status_code=status.HTTP_201_CREATED)
async def create_diary(
    diary_data: DiaryCreateInSchema, 
    current_user: User = Depends(get_current_active_user) # 로그인한 사용자만 작성 가능 jwt 토큰 검증
):
    """
    일기 작성
    - 로그인한 사용자만 작성 가능
    """
    diary = await Diary.create(
        title=diary_data.title,
        content=diary_data.content,
        user_id=current_user.id
    )
    return diary


@router.get("", response_model=List[DiaryOutSchema])
async def get_my_diaries(
    current_user: User = Depends(get_current_active_user), # 로그인한 사용자만 조회 가능 jwt 토큰 검증
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(10, ge=1, le=100, description="가져올 개수")
):
    """
    내 일기 목록 조회
    - 로그인한 사용자의 일기만 조회
    - 최신순으로 정렬
    """
    diaries = await Diary.filter(user_id=current_user.id).order_by('-created_at').offset(skip).limit(limit).all() # 로그인한 사용자의 일기만 skip으로 건너뛸 갯수 limit 조회
    return diaries


@router.get("/all", response_model=List[DiaryOutSchema])
async def get_all_diaries(
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(10, ge=1, le=100, description="가져올 개수")
):
    """
    모든 일기 조회 (공개용)
    - 인증 불필요
    - 최신순으로 정렬
    """
    diaries = await Diary.all().order_by('-created_at').offset(skip).limit(limit) # 모든 일기를 최신순으로 정렬하고 건너뛸 갯수 limit 조회
    return diaries


@router.get("/{diary_id}", response_model=DiaryOutSchema)
async def get_diary(diary_id: int):
    """
    특정 일기 조회
    - 인증 불필요
    """
    diary = await Diary.get_or_none(id=diary_id)
    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="일기를 찾을 수 없습니다."
        )
    return diary


@router.put("/{diary_id}", response_model=DiaryOutSchema)
async def update_diary(
    diary_id: int,
    diary_data: DiaryUpdateInSchema,
    current_user: User = Depends(get_current_active_user)
):
    """
    일기 수정
    - 작성자만 수정 가능
    """
    diary = await Diary.get_or_none(id=diary_id)
    
    if not diary: # 일기가 없으면 404 오류
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="일기를 찾을 수 없습니다."
        )
    
    if diary.user_id != current_user.id: # 일기 작성자가 아니면 403 오류
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="자신의 일기만 수정할 수 있습니다."
        )
    
    # 수정할 필드만 업데이트
    update_data = diary_data.dict(exclude_unset=True)
    if update_data:
        await diary.update_from_dict(update_data).save() 
    
    return diary


@router.delete("/{diary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diary(
    diary_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """
    일기 삭제
    - 작성자만 삭제 가능
    """
    diary = await Diary.get_or_none(id=diary_id)
    
    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="일기를 찾을 수 없습니다."
        )
    
    if diary.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="자신의 일기만 삭제할 수 있습니다."
        )
    
    await diary.delete()
    return None

