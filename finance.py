# selenium : 웹브라우저 조작 및 크롤링
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
# BeautifulSoup : 해당 페이지 정보를 가져옴
from bs4 import BeautifulSoup
# pandas : 데이터프레임 생성시 사용
import pandas as pd

print("주식 데이터 받아 (정적 웹) 웹에서 열고 조작(동적 웹)")

# 크롬 옵션에서 제한기간 옵션을 제외시켜 설정
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# webdriver 초기화
driver = webdriver.Chrome(options=chrome_options)

no = [] # 순위
name = [] # 종목명
price = [] # 현재가
full_time_cost = [] # 전일비
fluctuation_rate = [] # 등락률
par_value = [] # 액면가
sales = [] # 매출액
operating_profit = [] # 영업이익
net_income = [] # 당기순이익

for page in range(1, 11):
    # 네이버 증권 페이지 열기
    url = "https://finance.naver.com/sise/sise_market_sum.naver?&page={}".format(page)
    driver.get(url)

    if page == 1:
        list = [1, 4, 5, 6, 12, 15, 17, 21, 22]
        for i in list:
            element = driver.find_element(By.ID, "option{}".format(i))
            element.click()

        element = driver.find_element(By.XPATH, '//*[@id="contentarea_left"]/div[2]/form/div/div/div/a[1]')
        element.click()

    soup = BeautifulSoup(driver.page_source, "lxml")

    data_rows = soup.find("table", attrs={"class":"type_2"}).find("tbody").find_all("tr")
    for row in data_rows:
        columns = row.find_all("td")
        if len(columns) <= 1: # 의미 없는 데이터는 스킵
            continue

        data = [column.get_text().strip() for column in columns]
        data.pop()

        no.append(data[0])
        name.append(data[1])
        price.append(data[2])
        full_time_cost.append(data[3])
        fluctuation_rate.append(data[4])
        par_value.append(data[5])
        sales.append(data[6])
        operating_profit.append(data[7])
        net_income.append(data[8])

no_dict = {index: value for index, value in enumerate(no)}
name_dict = {index: value for index, value in enumerate(name)}
price_dict = {index: value for index, value in enumerate(price)}
full_time_cost_dict = {index: value for index, value in enumerate(full_time_cost)}
fluctuation_rate_dict = {index: value for index, value in enumerate(fluctuation_rate)}
par_value_dict = {index: value for index, value in enumerate(par_value)}
sales_dict = {index: value for index, value in enumerate(sales)}
operating_profit_dict = {index: value for index, value in enumerate(operating_profit)}
net_income_dict = {index: value for index, value in enumerate(net_income)}

df = pd.DataFrame({
    "N" : no_dict,
    "종목명" : name_dict,
    "현재가" : price_dict,
    "전일비" : full_time_cost_dict,
    "등락률" : fluctuation_rate_dict  ,  
    "액면가" : par_value_dict ,      
    "매출액" : sales_dict,
    "영업이익" : operating_profit_dict,
    "당기순이익" : net_income_dict
})

print(df)

df.loc[5, "종목명"] = "테스트 종목"
df.loc[5, "현재가"] = "12345678"
df.to_csv("data.csv", index=False, encoding="utf-8-sig")
print(df)

# 데이터프레임을 엑셀 파일로 저장
df.to_excel('시가총액1-500.xlsx', index=False, engine='openpyxl')

print("프로그램 종료")
driver.quit()