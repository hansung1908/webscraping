# selenium : 웹브라우저 조작 및 크롤링
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# BeautifulSoup : 해당 페이지 정보를 가져옴
from bs4 import BeautifulSoup
# pandas : 데이터프레임 생성을 위한 라이브러리
import pandas as pd
# time : 시간 지연시 사용
import time
# folium : 지도 및 마커 출력
import folium
# geopy : 주소를 통해 좌표 찾기
import geopy.geocoders
from geopy.geocoders import Nominatim
# 인증서 관련 문제 해결을 위한 라이브러리
import certifi
import ssl

print("부동산 데이터 받아 지역별로 분류, 지도 표시(동적 웹)")

# geopy ssl 오류를 해결하기 위해 인증서 갱신
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

# 크롬 옵션에서 제한기간 옵션을 제외시켜 설정
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# ssl 인증 파싱 문제를 막기 위해 설정
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# webdriver 초기화
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window() # 창 크기 최대화

driver.get("https://www.r114.com/?_c=memul&_m=p10&fCode=A&tabGbn=1")

name = [] # 아파트 이름
area = [] # 집 면적
dealing = [] # 매매시세
dealing_avg = [] # 평균매매
charter = [] # 전세시세
charter_avg = [] # 평균전세

temp_dealing_avg = [] # 지역별 아파트 비교를 위한 평균매매값 임시 저장소

# 지역 선택을 위한 조작
def place(a, b, c):
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="addressTitle"]/a').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="msrch_wrap_selectarea_Addr"]/li[{}]/a'.format(a)).click() # 시 선택
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="msrch_wrap_selectarea_Addr"]/li[{}]/a'.format(b)).click() # 구 선택
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="msrch_wrap_selectarea_Addr"]/li[{}]/a'.format(c)).click() # 동 선택
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="div_selectAddrTotal"]/a').click() # 찾기 클릭
    time.sleep(2)

# 아파트 정보 크롤링을 위한 메소드
def crawling():
    # 페이지 로딩 딜레이를 기다리기 위한 딜레이
    time.sleep(1)

    # 현재 페이지 데이터 크롤링
    soup = BeautifulSoup(driver.page_source, "lxml")

    # 아파트 정보가 담김 테이블의 행들 저장
    data_rows = soup.find("table", attrs={"class":"tbl_type2 typeA"}).find("tbody").find_all("tr")

    for row in data_rows:
        # 각 행의 요소들 저장
        columns = row.find_all("td")

        if len(columns) <= 1: # 의미 없는 데이터는 스킵
            continue

        # 각 요소들의 값을 빼서 리스트로 저장
        data = [column.get_text().strip() for column in columns]
        # 매매 평균값을 구하기 위한 정수화
        a1, a2 = data[2].replace(",", "").replace(" ", "").split("~")
        a3 = str((int(a1) + int(a2)) // 2)
        # 기존의 쓸모없는 데이터에 덧씌우기
        data[3] = a3

        # 전세 평균값을 구하기 위한 정수화
        b1, b2 = data[4].replace(",", "").replace(" ", "").split("~")
        b3 = str((int(b1) + int(b2)) // 2)
        # 기존의 쓸모없는 데이터에 덧씌우기
        data[5] = b3

        # 필요없는 열 삭제
        del data[6:]

        # 각각의 값을 종류별 리스트로 저장
        name.append(data[0])
        area.append(data[1])
        dealing.append(data[2])
        dealing_avg.append(data[3])
        charter.append(data[4])
        charter_avg.append(data[5])

        # 지역별 데이터 선별을 위한 리스트 저장
        temp_dealing_avg.append(data[3])

# 페이지 버튼 클릭을 위한 메소드, 해당 메소드가 나타날때 까지 대기
def page_click(i):
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="body_layout"]/div/div[5]/div[2]/div[3]/a[{}]'.format(i))))
    element.click()

# 페이지 버튼은 화면에 나타나지 않으면 인식이 안되므로 해당 페이지 버튼이 보이게 해당 좌표까지 강제로 스크롤 다운
def page_down():
    driver.execute_script("window.scrollTo(0, 1500);")
    time.sleep(1) # 스크롤 딜레이

# 페이지 버튼 누락시 보이게 하기 위한 새로고침
def refresh():
    driver.refresh()
    time.sleep(3) # 새로고침 딜레이

# 지도와 마커를 표시를 위한 메소드
def mapmarker(address, name, price, latitude, longitude):
    # 좌표 데이터를 바탕으로 지도 생성
    m = folium.Map(location=[latitude, longitude],
                zoom_start=17,
                width=750,
                height=500)
    
    # 좌표 데이터를 바탕으로 마우스를 대면 아파트 이름, 클릭하면 가격이 보이는 마커 생성
    folium.Marker([latitude, longitude],
                    popup=price,
                    tooltip=name).add_to(m)

    # 해당 지도를 지역이름이 붙혀진 html 파일로 저장
    m.save("{}.html".format(address))

# 주소를 좌표로 변환하는 함수
def address_to_coordinates(address):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(address)
    if location is not None:
        coordinates = (location.latitude, location.longitude)
        return coordinates
    else:
        return None

# 좌표를 받고 지도를 생성하기 위한 메소드, 기존 메소드를 결합해 더욱 간소화
def make_map(address, name, price):
    # 주소를 좌표로 변환
    coordinates = address_to_coordinates(address)

    if coordinates is not None:
        print(f"입력한 주소의 좌표: {coordinates[0]}, {coordinates[1]}")
    else:
        print("주소를 찾을 수 없습니다.")

    mapmarker(address, name, price, coordinates[0], coordinates[1])


place(1, 1, 9) # 강남구 압구정동
refresh()
for i in range(1, 6):
    crawling()
    page_down()
    page_click(i)

# 강남구 압구정동 아파트별 가격대 저장
gangnam_dealing_avg_dict = {index: int(value) for index, value in enumerate(temp_dealing_avg)}
# 이후 다른 지역 데이터를 넣기 위해 삭제
temp_dealing_avg.clear()

place(1, 9, 1) # 노원구 공릉동
refresh()
for i in range(1, 6):
    crawling()
    page_down()
    page_click(i)

# 노원구 공릉동 아파트별 가격대 저장, 이때 인덱스 값에 앞서 추가했었던 강남구 압구정동 아파트 수만큼 인덱스 값에 저장
# 해당 아파트 데이터 출력시 한꺼번에 저장되어 있는 데이터 프레임에서 꺼내기 위해 인덱스값 구별
nowon_dealing_avg_dict = {index + 75: int(value) for index, value in enumerate(temp_dealing_avg)}
temp_dealing_avg.clear()

place(1, 5, 3) # 관악구 신림동
refresh()
for i in range(1, 6):
    crawling()
    page_down()
    page_click(i)

# 관악구 신림동 아파트별 가격대 저장, 앞서 추가했던 아파트 수만큼 추가
gwanak_dealing_avg_dict = {index + 150: int(value) for index, value in enumerate(temp_dealing_avg)}
temp_dealing_avg.clear()

# 데이터 프레임 생성을 위한 딕셔너리화
name_dict = {index: value for index, value in enumerate(name)}
area_dict = {index: value for index, value in enumerate(area)}
dealing_dict = {index: value for index, value in enumerate(dealing)}
dealing_avg_dict = {index: value for index, value in enumerate(dealing_avg)}
charter_dict = {index: value for index, value in enumerate(charter)}
charter_avg_dict = {index: value for index, value in enumerate(charter_avg)}

# 데이터 프레임 생성
df = pd.DataFrame({
    "아파트 이름" : name_dict,
    "집 면적" : area_dict,
    "매매시세" : dealing_dict,
    "평균매매" : dealing_avg_dict,
    "전세시세" : charter_dict,
    "평균전세" : charter_avg_dict
})

print(df)

# 각 지역별 아파트 평균매매가격을 비교하여 가장 큰 가격의 아파트에 대한 정보를 데이터프레임에서 가져와 지도 생성
gangnam_max_key = max(gangnam_dealing_avg_dict, key=gangnam_dealing_avg_dict.get)
gangnam_max_row_data = df.iloc[gangnam_max_key].tolist()
make_map('강남구 압구정동', gangnam_max_row_data[0], gangnam_max_row_data[3])

nowon_max_key = max(nowon_dealing_avg_dict, key=nowon_dealing_avg_dict.get)
nowon_max_row_data = df.iloc[nowon_max_key].tolist()
make_map('노원구 공릉동', nowon_max_row_data[0], nowon_max_row_data[3])

gwanak_max_key = max(gwanak_dealing_avg_dict, key=gwanak_dealing_avg_dict.get)
gwanak_max_row_data = df.iloc[gwanak_max_key].tolist()
make_map('관악구 신림동', gwanak_max_row_data[0], gwanak_max_row_data[3])

driver.quit()

while True:
    try:
        # 지역 이름, 최소값, 최대값을 입력
        area_name, min_price, max_price = \
            input("원하는 지역(압구정, 공릉, 신림 중)에 최소, 최대 매매가격을 입력하시오(ex. 압구정 100000 200000) : ").split()
        # 입력받은 조건에 맞는 아파트를 찾아서 출력
        for key, value in name_dict.items():
            if area_name in value and min_price < dealing_avg_dict[key] and dealing_avg_dict[key] < max_price:
                print(df.iloc[key].tolist())
    except: # 잘못된 입력 시 설명과 함께 처음부터 다시 진행
        print("잘못된 입력입니다. 다시 입력해주세요.")
        continue
    
    # 그만하려면 y입력으로 무한루프 탈출
    quit = input("그만하시겠습니까?(y or n) : ")
    if quit == "y":
        break

print("프로그램 종료")