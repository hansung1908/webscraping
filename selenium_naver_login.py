from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

browser = webdriver.Chrome(options=chrome_options)
time.sleep(random.uniform(1,3)) # 자동화탐지를 우회 하기 위한 delay

# 1. 네이버 이동
browser.get("http://naver.com")

# 2. 로그인 버튼 클릭
element = browser.find_element(By.CLASS_NAME, "MyView-module__link_login___HpHMW")
element.click()

# 3. id, pw 입력
input_js = ' \
        document.getElementById("id").value = "{id}"; \
        document.getElementById("pw").value = "{pw}"; \
    '.format(id = "my_id", pw = "my_password") # captcha 탐지 우회를 위해 id, pw가 입력하는 js 생성, my_id my_password 대신 자신의 네이버 아이디 비밀번호를 입력
time.sleep(random.uniform(1,3)) # 자동화탐지를 우회 하기 위한 delay
browser.execute_script(input_js) # 만들었던 js파일을 브라우저에 적용

# 4. 로그인 버튼 클릭
time.sleep(random.uniform(1,3)) # 자동화탐지를 우회 하기 위한 delay
browser.find_element(By.ID, "log.login").click()

# 5. html 정보 출력
print(browser.page_source)

# 6. 브라우저 종료
browser.quit()