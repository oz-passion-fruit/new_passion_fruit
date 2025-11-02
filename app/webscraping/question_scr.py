import requests
import re
from bs4 import BeautifulSoup
from app.schemas.question import QuestionCreateInSchema 

url = "https://steemit.com/kr/@centering/1010"

all_questions_data = []

# 위장
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)


if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    question_candidates = soup.find_all(string=lambda text: text and '?' in text) # '?'가 포함되면 
    
    
    question_count = 0
    for candidate_text in question_candidates: 
        question_text = candidate_text.strip() # 공백 제거
        question_text = ' '.join(question_text.split()) # 여러 공백, 줄바꿈 등을 단일 공백으로 처리
    
        if len(question_text) > 0 and question_text.endswith('?'): # 물음표로 끝나면 추가
            all_questions_data.append(QuestionCreateInSchema(question=question_text))
            print(f'질문 : {question_text}')
            print()
    
    print(f"\n총 {len(all_questions_data)}개의 질문을 수집했습니다.")
else:
    print(f"페이지 로딩 실패. 상태 코드: {response.status_code}")


import asyncio
from app.db.database import init_db
from app.db.models.question import Question
from app.schemas.question import QuestionCreateInSchema # 질문 생성 스키마

async def save_questions_to_db():
    await init_db()
    for question_data in all_questions_data: # all_questions_data를 사용
        await Question.create(**question_data.model_dump()) # QuestionCreateInSchema 객체의 model_dump() 사용
    print("데이터베이스에 질문 저장 완료")

if __name__ == "__main__":
    asyncio.run(save_questions_to_db())
