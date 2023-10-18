# selenium : 웹브라우저 조작 및 크롤링
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# BeautifulSoup : 해당 페이지 정보를 가져옴
from bs4 import BeautifulSoup
# pandas : 데이터프레임 생성을 위한 라이브러리
import pandas as pd
# matplotlib : 그래프 생성을 위한 라이브러리
import matplotlib.pyplot as plt

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window() # 창 크기 최대화

url ="https://flight.naver.com/"
driver.get(url)

# 가는 날 클릭
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[4]/div/div/div[2]/div[2]/button[1]').click()

# 이번달 25일, 26일 클릭
driver.find_elements(By.XPATH, '//b[text() ="25"]')[0].click() # [0] = 이번달
driver.find_elements(By.XPATH, '//b[text() ="26"]')[0].click()

# 도착지 선택
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[4]/div/div/div[2]/div[1]/button[2]').click()
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[10]/div[1]/div/input').send_keys("도쿄")
time.sleep(1)
driver.find_element(By.XPATH, '//i[contains(text(),"나리타국제공항")]').click()

# 항공권 검색 클릭
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[4]/div/div/div[2]/button').click()

# xpath 값이 위치할때까지 지연, 최대 지연시간은 10초
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "concurrent_select_schedule__3O1pT")))

# 현제 페이지 데이터 크롤링
soup = BeautifulSoup(driver.page_source, "lxml")

# 각 요소를 종류별로 모아서 저장
names = soup.find_all("div", attrs={"class":"airline"})
start_times = soup.find_all("b", attrs={"class":"route_time__-2Z1T"})
prices = soup.find_all("i", attrs={"class":"item_num__3R0Vz"})

# 모은 요소들에서 값만 빼다 리스트화
name_list = [name.get_text().strip() for name in names]
start_time_list = [start_time.get_text().strip() for start_time in start_times]
price_list = [price.get_text().strip() for price in prices]

# 모든 요소를 다 수집하여 필요 이상에 데이터가 수집되어 조건에 맞게 30이후의 데이터는 삭제
del name_list[30:]
del start_time_list[30:]
del price_list[30:]

# 데이터프레임 생성을 위한 딕셔너리화
name_dict = {index: value for index, value in enumerate(name_list)}
start_time_dict = {index: value for index, value in enumerate(start_time_list)}
price_dict = {index: value for index, value in enumerate(price_list)}

# 데이터프레임 생성
df = pd.DataFrame({
    "항공사" : name_dict,
    "출발시간" : start_time_dict,
    "가격" : price_dict
})

print(df)

# 인덱스 2번에 해당 값들로 변경
name_list[2] = "테스트 제목"
start_time_list[2] = "12345678"

# 그래프 생성을 위한 준비
# 한글 깨짐을 방지하기 위해 폰트와 문자 인코딩 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
# x값 출력시 겹치는 것을 방지하기 위해 90도 돌려 출력
plt.xticks(rotation=90)
# y값에 범위를 정해 출력
plt.ylim(300000, 450000)

# 세 개의 리스트를 문자열로 합칩니다.
combined_list = [f"{a} {b} {c}" for a, b, c in zip(name_list, start_time_list, price_list)]

# 범위를 설정하기 위해 가격 부분을 정수화
int_price_list = [int(val.replace(",", "")) for val in price_list]

# 바 그래프로 설정 및 출력
plt.bar(combined_list, int_price_list)
plt.show()

print("프로그램 종료")
driver.quit()