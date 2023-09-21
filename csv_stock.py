import csv
import requests
from bs4 import BeautifulSoup

url= "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page="

filename = "시가총액1-200.csv"
f = open(filename, "w", encoding="utf-8-sig", newline="") # newline="" 은 각 라인 사이에 공백을 출력하라는 뜻, excel 파일의 경우 encoding="utf-8-sig"
writer = csv.writer(f)

title = "N	종목명	현재가	전일비	등락률	액면가	시가총액	상장주식수	외국인비율	거래량	PER	ROE".split("\t") # \t를 구분자로 하여 리스트 구성
writer.writerow(title)

for page in range(1, 5):
    res = requests.get(url + str(page))
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    data_rows = soup.find("table", attrs={"class":"type_2"}).find("tbody").find_all("tr")
    for row in data_rows:
        columns = row.find_all("td")
        if len(columns) <= 1: # 의미 없는 데이터는 스킵
            continue
        data = [column.get_text().strip() for column in columns]
        writer.writerow(data) # writerow를 쓰기 위해선 list타입의 입력값 필수
