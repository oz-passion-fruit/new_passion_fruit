from fastapi import APIRouter, HTTPException, status, Query
from typing import List
import random

from app.schemas.question import QuestionOutSchema
from app.db.models.question import Question

router = APIRouter(prefix="/questions", tags=["질문"])


@router.get("", response_model=List[QuestionOutSchema]) 
async def get_questions(
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(10, ge=1, le=100, description="가져올 개수")
):
    """
    질문 목록 조회
    - 인증 불필요
    - 최신순으로 정렬
    """
    questions = await Question.all().offset(skip).limit(limit)
    return questions


@router.get("/random", response_model=QuestionOutSchema)
async def get_random_question():
    """
    랜덤 질문 1개 조회
    - 매번 다른 질문을 랜덤하게 반환
    """
    # 전체 질문 개수 조회
    total_count = await Question.all().count()
    
    if total_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="등록된 질문이 없습니다."
        )
    
    # 랜덤 인덱스 생성
    random_offset = random.randint(0, total_count - 1)
    
    # 랜덤 질문 가져오기
    question = await Question.all().offset(random_offset).limit(1).first()
    
    return question


@router.get("/{question_id}", response_model=QuestionOutSchema)
async def get_question(question_id: int):
    """
    특정 질문 조회
    """
    question = await Question.get_or_none(id=question_id)
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="질문을 찾을 수 없습니다."
        )
    
    return question


@router.get("/count/total")
async def get_questions_count():
    """
    전체 질문 개수 조회
    """
    count = await Question.all().count()
    return {"total": count}

