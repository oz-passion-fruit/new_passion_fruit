from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
import random

from app.schemas.quotes import QuoteOutSchema
from app.db.models.quotes import Quote

router = APIRouter(prefix="/quotes", tags=["명언"])


@router.get("", response_model=List[QuoteOutSchema])
async def get_quotes(
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(10, ge=1, le=100, description="가져올 개수"),
    author: Optional[str] = Query(None, description="작가 이름으로 필터링")
):
    """
    명언 목록 조회
    - 인증 불필요
    - 작가별 필터링 가능
    """
    if author:
        quotes = await Quote.filter(author__icontains=author).offset(skip).limit(limit).all()
    else:
        quotes = await Quote.all().offset(skip).limit(limit)
    
    return quotes


@router.get("/random", response_model=QuoteOutSchema)
async def get_random_quote():
    """
    랜덤 명언 1개 조회
    - 매번 다른 명언을 랜덤하게 반환
    """
    # 전체 명언 개수 조회
    total_count = await Quote.all().count()
    
    if total_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="등록된 명언이 없습니다."
        )
    
    # 랜덤 인덱스 생성
    random_offset = random.randint(0, total_count - 1)
    
    # 랜덤 명언 가져오기
    quote = await Quote.all().offset(random_offset).limit(1).first()
    
    return quote


@router.get("/authors", response_model=List[dict])
async def get_authors():
    """
    모든 작가 목록 조회
    - 중복 제거된 작가 이름 리스트 반환
    """
    quotes = await Quote.all().values('author')
    
    # 중복 제거 및 None 값 제외
    authors = list(set([q['author'] for q in quotes if q['author'] is not None]))
    authors.sort()
    
    return [{"author": author} for author in authors]


@router.get("/{quote_id}", response_model=QuoteOutSchema)
async def get_quote(quote_id: int):
    """
    특정 명언 조회
    """
    quote = await Quote.get_or_none(id=quote_id)
    
    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="명언을 찾을 수 없습니다."
        )
    
    return quote


@router.get("/count/total")
async def get_quotes_count():
    """
    전체 명언 개수 조회
    """
    count = await Quote.all().count()
    return {"total": count}

