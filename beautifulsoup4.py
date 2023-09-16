import requests
from bs4 import BeautifulSoup

url = "https://land.naver.com/"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")
print(soup.title)
print(soup.title.get_text())
print(soup.a) # soup 객체에서 처음 발견되는 div element 출력
print(soup.a.attrs) # div element의 속성 정보를 출력
print(soup.a["href"]) # div element의 id 속성 '값' 정보를 출력

print(soup.find("a", attrs={"class":"type_admin NPI=a:landad"})) # class="type_admin NPI=a:landad"인 span element를 찾기
print(soup.find(attrs={"class":"type_admin NPI=a:landad"})) # # class="type_admin NPI=a:landad"인 어떤 element 찾기

item1 = soup.find("li", attrs={"class":"item_area"})
print(item1.get_text())
print(item1.next_sibling) # 다음 리스트 요소로 이동, 중간에 개행을 위한 줄바꿈 정보가 있어 공백 출력
item2 = item1.next_sibling.next_sibling # 2번의 이동으로 다음 리스트 요소 출력, 두번째 정보
item3 = item2.next_sibling.next_sibling # 세번째 정보
print(item2.get_text())
print(item3.get_text())
item4 = item3.previous_sibling.previous_sibling # 2번의 이동으로 이전 리스트 요소 출력, 두번째 요소
print(item4.get_text())

item2 = item1.find_next_sibling("li") # 해당 객체를 기준으로 li태그가 나올때까지 다음으로 이동
print(item2.get_text())
item3 = item2.find_next_sibling("li")
print(item3.get_text())
item4 = item3.find_previous_sibling("li")
print(item4.get_text())

print(item1.find_next_siblings("li")) # 모든 li태그를 가진 요소 출력

print(item1.parent) # 해당 요소의 상위 요소로 접근, 리스트 전체를 출력

text = soup.find("span", text="가용자금 확인 및 대출 계획")
print(text)