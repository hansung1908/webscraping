import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

browser = webdriver.Chrome(options=chrome_options)
browser.maximize_window() # 창 크기 최대화

# 페이지 이동
url = "https://play.google.com/store/games"
browser.get(url)

# 지정한 위치로 스크롤 내리기
# 모니터(해상도) 높이인 1080 위치만큼 스크롤 내리기
# browser.execute_script("window.scrollTo(0, 1080)") # 1920 x 1080

interval = 2 # 2초에 한번씩 스크롤 내림

# 현재 문서 높이를 가져와서 저장
prev_height = browser.execute_script("return document.body.scrollHeight")

# 반복 수행
while True:
    # 현재 문서가 로딩된 만큼에서 가장 아랫부분으로 스크롤 내리기
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    # 페이지 로딩 대기
    time.sleep(interval)

    # 현재 문서 높이를 가져와서 저장
    curr_height = browser.execute_script("return document.body.scrollHeight")
    if curr_height == prev_height:
        break

    # 문서 높이 갱신
    prev_height = curr_height

print("스크롤 완료")

soup = BeautifulSoup(browser.page_source, "lxml")

games = soup.find_all("div", attrs={"class" : "ULeU3b neq64b"})
print(len(games))

with open("game.html", "w", encoding="utf8") as f:
    # f.write(res.text)
    f.write(soup.prettify()) # html 문서를 양식에 맞게 출력, user-agent 정보를 넣어주지 않으면 영어권을 기준으로 복사

for game in games:
    try:
        # 제목
        title = game.find("span", attrs={"class" : "sT93pb DdYX5 OnEJge"}).get_text()

        # 평점
        rate = game.find_all("span", attrs={"class" : "w2kbF"})[1].get_text()

        # 링크
        link = game.find("a", attrs={"class" : "Si6A0c Gy4nib"})["href"]
        
        print(f"제목 : {title}")
        print(f"평점 : {rate}")
        print("링크 :", "https://play.google.com" + link)
        print("-"*50)
    except:
        print("error "*5)

browser.quit()