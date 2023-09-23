from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

browser = webdriver.Chrome(options=chrome_options)
browser.maximize_window() # 창 크기 최대화

url ="https://flight.naver.com/"
browser.get(url)

# 가는 날 클릭
browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[4]/div/div/div[2]/div[2]/button[1]').click()

# 이번달 25일, 26일 클릭
browser.find_elements(By.XPATH, '//b[text() ="25"]')[0].click() # [0] = 이번달
browser.find_elements(By.XPATH, '//b[text() ="26"]')[0].click()


# 도착지 선택
browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[4]/div/div/div[2]/div[1]/button[2]').click()
browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[10]/div[1]/div/input').send_keys("도쿄")
time.sleep(random.uniform(1,3))
browser.find_element(By.XPATH, '//i[contains(text(),"나리타국제공항")]').click()

# 항공권 검색 클릭
browser.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[4]/div/div/div[2]/button').click()


try:
    # xpath 값이 위치할때까지 지연, 최대 지연시간은 10초
    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[6]/div/div[3]/div[1]')))
    # 항공권 출력
    print(element.text)
finally:
    browser.quit()