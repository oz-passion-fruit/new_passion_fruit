from sqlalchemy import text
from db_session import SessionLocal
print("데이터베이스 연결 테스트를 시작합니다...")
db = None
try:
    db = SessionLocal()
    print("세션 생성 성공. (DB 서버와 통신 시작)")
    result = db.execute(text("SELECT 1"))
    print(f"쿼리 실행 성공. (결과: {result.fetchone()})")
    print("\n 데이터베이스 연결에 성공했습니다!")
except Exception as e:
    print("\n 데이터베이스 연결 또는 쿼리 실패.")
    print("--- 오류 메시지 ---")
    print(e)
finally:
    if db:
        db.close()
        print("\n세션이 닫혔습니다.")