import requests
import re
from bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Whale/3.22.205.18 Safari/537.36"}

for i in range(1, 6):
    url = "https://browse.gmarket.co.kr/search?keyword=%EB%85%B8%ED%8A%B8%EB%B6%81&k=30&p={}".format(i)

    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    items = soup.find_all("div", attrs={"class":re.compile("^box__component box__component-itemcard")})

    for item in items:
        name = item.find("span", attrs={"class":"text__item"}).get_text()
        price = item.find("strong", attrs={"class":"text text__value"}).get_text()
        link = item.find("a", attrs={"class":"link__item"})["href"]

        # 갤럭시 제품 제외
        if "갤럭시" in name:
            print("<갤럭시는 제외 상품입니다.>")
            continue

        # 100만원 이상만 조회
        if len(price) > 8:
            print(f"제품명 : {name}")
            print(f"가격 : {price}")
            print("바로가기 : {}".format(link))
            print("-"*100) # 줄 긋기