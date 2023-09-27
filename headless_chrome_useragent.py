import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# headless 설정, 브라우저를 띄우지 않고 동작을 실행
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")

# headless 설정시 user-agent가 headlesschorme으로 바뀌면서 서버에서 브라우저 접속을 차단할 수도 있어 필요시 해당 설정 사용
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Whale/3.22.205.18 Safari/537.36")

browser = webdriver.Chrome(options=chrome_options)
browser.maximize_window() # 창 크기 최대화

# 페이지 이동
url = "https://www.whatismybrowser.com/detect/what-is-my-user-agent/"
browser.get(url)

detected_value = browser.find_element(By.ID, "detected_value")
print(detected_value.text)
browser.quit()