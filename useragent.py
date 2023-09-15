import requests

url = "http://nadocoding.tistory.com"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Whale/3.22.205.18 Safari/537.36"}

res = requests.get(url, headers=headers)
res.raise_for_status()

with open("nadocoding.html", "w", encoding="utf-8") as f:
    f.write(res.text)

# user agent를 통해 403과 같은 접속 오류 문제를 해결
# what is my user agent? 사이트에 들어가 자신이 사용하는 브라우저에 맞는 user agent를 확인 가능
# user agent 값을 requests에 넣음으로써 문제를 해결