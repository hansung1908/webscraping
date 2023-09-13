import requests

# 해당 url로 부터 정보를 받아 res에 저장
res = requests.get("http://naver.com")
print("응답코드 :", res.status_code) # http 상태코드와 동일

res = requests.get("http://nadocoding.tistory.com")
print("응답코드 :", res.status_code)

if res.status_code == requests.codes.ok:
    print("정상입니다.")
else:
    print("문제가 생겼습니다. [에러코드 ", res.status_code, "]")

res.raise_for_status()
print("웹 스크래핑을 진행합니다.")

# res = requests.get("http://nadocoding.tistory.com")
# res.raise_for_status()
# 해당 url에서 제대로 정보를 가져오면 넘어가고 문제가 생기면 에러 발생
# 둘이 같이 많이 쓰므로 익혀둘 것

res = requests.get("http://google.com")
print(len(res.text))
print(res.text)

# mygoogle.html 파일을 생성하여 구글로부터 받은 화면 텍스트 정보를 저장
with open("mygoogle.html", "w", encoding="utf-8") as f:
    f.write(res.text)

