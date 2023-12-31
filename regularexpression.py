import re

p = re.compile("ca.e")
# . (ca.e) : 하나의 문자를 의미(case, cave, cafe / caffe (x))
# ^ (^de) : 문자열의 시작(desk, destination / fade (x)) 
# $ (se$) : 문자열의 끝(case, base / face (x))

def print_match(m):
    if m:
        print("m.group() : ", m.group()) # 일치하는 문자열 반환
        print("m.string : ", m.string) # 일치하는 문자열
        print("m.start() : ", m.start()) # 일치하는 문자열의 시작 index
        print("m.end() : ", m.end()) # 일치하는 문자열의 끝 index
        print("m.span() : ", m.span()) # 일치하는 문자열의 시작 / 끝 index
    else:
        print("매칭되지 않음")

m = p.match("careless") # match : 주어진 문자열의 처음부터 일치하는지 확인(careless -> care 로 출력)
print_match(m)

m = p.search("good care") # search : 주어진 문자열 중에 일치하는게 있는지 확인
print_match(m)

lst = p.findall("good care cafe") # findall : 일치하는 모든 것을 리스트 형태로 반환
print(lst)

# w3school 사이트에서 python regex, 파이썬 공식문서에서 regular expression에서 더 자세한 내용이 있으니 참조