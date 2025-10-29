from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # Options -> 클래스
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from bs4 import BeautifulSoup
from app.schemas.quotes import QuoteCreateSchema 

url = "https://quotes.toscrape.com/"

option_ = Options()
option_.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=option_)
driver.get(url) 
time.sleep(1)

all_quotes_data = [] # 모든 명언을 저장할 리스트

while True:
    # 페이지 스크롤 (필요하다면 유지, paginated 사이트에서는 불필요할 수도 있음)
    for _ in range(20):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    current_page_items = soup.select(".quote")
    for item in current_page_items:
        content = item.select_one(".text").text
        author = item.select_one(".author").text

        all_quotes_data.append(QuoteCreateSchema(content=content, author=author))
        
        print(f'내용 : {content}')
        print(f'작가 : {author}')
        print()

    if len(all_quotes_data) >= 100:
        print(f"목표한 명언 {len(all_quotes_data)}개 수집 완료.")
        break

    # 다음 페이지로 이동
    next_button = driver.find_elements(By.CSS_SELECTOR, ".next > a")
    if not next_button: # "Next" 버튼이 없으면 루프 종료
        print("더 이상 다음 페이지가 없습니다.")
        break
    
    next_button[0].click()
    time.sleep(2) # 다음 페이지 로드를 기다립니다.

driver.quit()


import asyncio
from app.db.database import init_db
from app.db.models.quotes import Quote
from app.schemas.quotes import QuoteInSchema

async def save_quotes_to_db():
    await init_db()
    for quote_data in all_quotes_data: # all_quotes_data를 사용
        await Quote.create(**quote_data.model_dump())
    print("데이터베이스에 명언 저장 완료")

if __name__ == "__main__":
    asyncio.run(save_quotes_to_db())

