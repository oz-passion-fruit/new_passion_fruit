from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from tortoise.contrib.fastapi import register_tortoise
import os

from app.core.config import ALLOWED_ORIGINS, DB_URL
from app.api.routes import auth, diary, question, quote

# FastAPI 앱 생성
app = FastAPI(
    title="Passion Fruit API",
    description="일기, 질문, 명언 서비스 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router, prefix="/api")
app.include_router(diary.router, prefix="/api")
app.include_router(question.router, prefix="/api")
app.include_router(quote.router, prefix="/api")

# Tortoise ORM 등록
register_tortoise(
    app,
    db_url=DB_URL,
    modules={"models": [
        "app.db.models.user",
        "app.db.models.question",
        "app.db.models.diary",
        "app.db.models.quotes"
    ]},
    generate_schemas=True,  # 개발 환경에서만 True, 운영환경에서는 False
    add_exception_handlers=True,
)


@app.get("/health")
async def health_check():
    """
    헬스 체크 엔드포인트
    """
    return {"status": "healthy"}


# 프론트엔드 정적 파일 서빙
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

# CSS, JS 등 정적 파일
app.mount("/css", StaticFiles(directory=os.path.join(frontend_path, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(frontend_path, "js")), name="js")


# HTML 파일 라우트
@app.get("/")
async def index():
    """메인 페이지"""
    return FileResponse(os.path.join(frontend_path, "index.html"))


@app.get("/auth.html")
async def auth():
    """로그인/회원가입 페이지"""
    return FileResponse(os.path.join(frontend_path, "auth.html"))


@app.get("/diary.html")
async def diary_page():
    """일기 페이지"""
    return FileResponse(os.path.join(frontend_path, "diary.html"))


@app.get("/question.html")
async def question_page():
    """질문 페이지"""
    return FileResponse(os.path.join(frontend_path, "question.html"))


@app.get("/quote.html")
async def quote_page():
    """명언 페이지"""
    return FileResponse(os.path.join(frontend_path, "quote.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

