import requests
import re
from bs4 import BeautifulSoup
from app.schemas.question import QuestionInSchema 

url = "https://steemit.com/kr/@centering/1010"

all_questions_data = []

print("스팀잇 페이지에서 질문을 가져오는 중...")

# requests를 사용하여 페이지 가져오기 (Selenium보다 간단하고 빠름)
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 전체 텍스트에서 직접 추출 (페이지 구조와 관계없이)
    text_content = soup.get_text()
    
    # 본문 시작 부분 찾기 (불필요한 헤더 제거)
    start_marker = "그러고 보니 요즘에는 질문이 가득담겨 있는 책들이 정말 많네요."
    if start_marker in text_content:
        text_content = text_content.split(start_marker)[1]
    
    # 정규식으로 물음표로 끝나는 문장 추출
    # 패턴: 문장 시작부터 물음표까지 (최소 10자 이상)
    pattern = r'([^?\n]{10,}?\?)'
    matches = re.findall(pattern, text_content)
    
    print(f"정규식으로 {len(matches)}개의 질문 패턴 발견")
    
    question_count = 0
    for question_text in matches:
        # 질문 텍스트 정리 (불필요한 공백과 줄바꿈 제거)
        question_text = question_text.strip()
        question_text = ' '.join(question_text.split())
        
        # 유효한 질문인지 확인
        # - 길이가 적절하고
        # - 한글이 포함되어 있고
        # - 너무 긴 문장이 아닌 경우 (500자 이하)
        if (question_text and 
            len(question_text) > 10 and 
            len(question_text) < 500 and
            any('\uac00' <= char <= '\ud7a3' for char in question_text)):  # 한글 포함 확인
            
            question_count += 1
            all_questions_data.append(QuestionInSchema(question=question_text))
            print(f'{question_count}. {question_text[:100]}{"..." if len(question_text) > 100 else ""}')
    
    print(f"\n총 {len(all_questions_data)}개의 질문을 수집했습니다.")
else:
    print(f"페이지 로딩 실패. 상태 코드: {response.status_code}")


import asyncio
from app.db.database import init_db
from app.db.models.question import Question
from app.schemas.question import QuestionInSchema

async def save_questions_to_db():
    await init_db()
    for question_data in all_questions_data: # all_questions_data를 사용
        await Question.create(**question_data.model_dump())
    print("데이터베이스에 질문 저장 완료")

if __name__ == "__main__":
    asyncio.run(save_questions_to_db())
