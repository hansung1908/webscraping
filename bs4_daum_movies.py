import requests
from bs4 import BeautifulSoup

for year in range(2015, 2023):
    url = "https://search.daum.net/search?w=tot&q={}%EB%85%84%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&DA=MOR&rtmaxcoll=MOR".format(year)
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")

    images = soup.find_all("img", attrs={"class":"thumb_img"})

    for index, img in enumerate(images):
        image_url = img["src"]

        if image_url.startswith("//"):
            img = "https:" + image_url

        print(img["src"])

        image_res = requests.get(image_url)
        image_res.raise_for_status()

        # wb : write binary, 글자가 아닌 이미지를 쓸때
        with open("movie_{}_{}.jpg".format(year, index+1), "wb") as f:
            f.write(image_res.content)

        if index >= 4: # 상위 5개 이미지만 다운로드
            break