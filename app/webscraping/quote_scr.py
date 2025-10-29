import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import requests
from bs4 import BeautifulSoup
from app.schemas.quotes import QuoteCreateInSchema 

base_url = "https://quotes.toscrape.com"
all_quotes_data = []
page = 1

while len(all_quotes_data) < 100:
    url = f"{base_url}/page/{page}/" if page > 1 else base_url
    
    response = requests.get(url)
    if response.status_code != 200:
        print("더 이상 페이지가 없습니다.")
        break
    
    soup = BeautifulSoup(response.text, "html.parser")
    current_page_items = soup.select(".quote")
    
    if not current_page_items:
        break
    
    for item in current_page_items:
        content = item.select_one(".text").text
        author = item.select_one(".author").text
        
        all_quotes_data.append(QuoteCreateInSchema(content=content, author=author))
        
        print(f'내용 : {content}')
        print(f'작가 : {author}')
        print()
        
        if len(all_quotes_data) >= 100:
            break
    
    page += 1

print(f"총 {len(all_quotes_data)}개 명언 수집 완료.")


import asyncio
from app.db.database import init_db
from app.db.models.quotes import Quote
from app.schemas.quotes import QuoteOutSchema

async def save_quotes_to_db():
    await init_db()
    for quote_data in all_quotes_data:
        await Quote.create(**QuoteOutSchema.model_dump(quote_data)) # model_dump() 메서드를 사용하여 스키마에 맞게 데이터 변환
    print("데이터베이스에 명언 저장 완료")

if __name__ == "__main__":
    asyncio.run(save_quotes_to_db())