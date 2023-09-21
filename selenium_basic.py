from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

browser = webdriver.Chrome(options=chrome_options) # selenium manager라는 드라이버 관리 프로그램이 연동되어 chromedriver.exe 파일을 다운받지 않아도 실행하면 알아서 다운
browser.get("http://naver.com")

# 터미널에서 테스트(python(), 종료는 exit())
from selenium.webdriver.common.by import By
# 해당 브라우저에서 로그인 버튼 요소를 받아 element에 저장
element = browser.find_element(By.CLASS_NAME, "MyView-module__link_login___HpHMW")

element.click() # 해당 요소를 클릭
browser.back() # 해당 브라우저를 뒤로가기
browser.forward() # 해당 브라우저를 앞으로가기
browser.refresh() # 해당 브라우저 새로고침

element = browser.find_element(By.ID, "query") # 검색창 요소를 받아 저장 
from selenium.webdriver.common.keys import Keys
element.send_keys("나도코딩") # 검색창에 "나도코딩" 입력
element.send_keys(Keys.ENTER) # enter 클릭

element = browser.find_element(By.TAG_NAME, "a") # 가장 처음에 있는 a 태그 요소를 저장, find_elements로 하면 모든 a 태그 요소 저장
for e in element:
    e.get_attribute("href") # element가 가지는 요소들 중 href 속성만 추출

browser.get("http://daum.com") # daum으로 이동
element = browser.find_element(By.NAME, "q") # name 태그가 q인 가장 처음 요소 저장(다음 검색창)
element = browser.find_element(By.XPATH, "//*[@id='daumSearch']/fieldset/div/div/button[3]") # xpath를 통해 검색 버튼 요소 저장, xpath 중간 ""는 ''로 변경

browser.close() # 현재 브라우저 탭만 종료
browser.quit() # 브라우저 전체 종료