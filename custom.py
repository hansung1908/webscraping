# selenium : 웹브라우저 조작 및 크롤링
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
# time : 시간 지연시 사용
import time
# urllib : 이미지 저장시 사용
import urllib.request

# 추가 기능들을 위해 임포트
# 이미지 정보를 읽기 위해 사용
from PIL import Image
import cv2
# 이미지 파일 위치 이동시 사용
import shutil
# 이미지 색 추출을 위해 사용
from colorthief import ColorThief
# 이미지에서 배경만 지우기 위해 사용
from rembg import remove
# 이미지 rgb값을 배열로 받기 위해 사용
import numpy as np

print("selenium을 활용한 이미지 크롤링 + 다양한 기능을 추가한 고도화 버전")

# 크롬 옵션에서 제한기간 옵션을 제외시켜 설정
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# webdriver 초기화
driver = webdriver.Chrome(options=chrome_options)

# 구글 이미지 검색 페이지 열기
driver.get("https://www.google.com/imghp?hl=ko&tab=ri&ogbl")

# 검색어 입력
elem = driver.find_element(By.NAME, "q") # name태그 값이 q(검색창)인 요소 찾아 저장
elem.send_keys("강아지") # 강아지 입력
elem.send_keys(Keys.RETURN) # 엔터키 클릭

elem = driver.find_element(By.TAG_NAME, "body") # 페이지 전체를 저장

for i in range(10):
    elem.send_keys(Keys.PAGE_DOWN) # 스크롤 다운을 통한 더 많은 사진 로딩
    time.sleep(0.1) # 너무 빠른 스크롤 다운으로 인한 오류 방지를 위해 딜레이 조정
time.sleep(3)

images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd") # 개발자 도구로 가져온 클래스 내용값은 .이 누락되므로 주의

forbid = 0

actions = ActionChains(driver) # 마우스 컨트롤을 위한 설정

for index, image in enumerate(images):
    try:
        actions.move_to_element(image).click(image).perform() # 마우스 커서를 이미지로 썸네일 이미지로 가져가 클릭
        time.sleep(1)
        
        # 클릭 후 나온 큰 이미지의 링크 주소를 xpath를 통해 저장
        imageUrl = driver.find_element(By.XPATH, '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]').get_attribute("src")
        urllib.request.urlretrieve(imageUrl, "small\\" + str(index-forbid) + ".jpg") # 저장한 url을 가져와 jpg 이미지로 저장

        # 크롤링한 이미지에서 배경을 지워 따로 저장, 강아지 사진만 남게 저장
        input = Image.open("small\\" + str(index-forbid) + ".jpg")
        output = remove(input) # rembg 라이브러리의 remove메소드를 통해 자체 프로그램이 배경을 인식하여 삭제
        output.save("fix\\" + str(index-forbid) + "_fix.png") # 강아지 사진만 남은 이미지 fix 폴더에 저장

        # 배경 지운 강아지 이미지에서 가장 많은 부분을 차지하는 색상 rgb값 추출
        ct = ColorThief("fix\\" + str(index-forbid) + "_fix.png") # 이미지의 색상 정보 추출
        rgb = ct.get_color(quality=1) # 이미지에서 가장 많이 나온 색상 1가지만 추출

        data = np.zeros((128, 128, 3), np.uint8) # 추출한 색상을 이미지화하기 위해 128x128 사이즈의 배열 준비
        data[:,:] = [rgb[0], rgb[1], rgb[2]] # rgb 배열값 입력
        
        image = Image.fromarray(data, mode="RGB") # data에 저장된 정보를 바탕으로 색상 이미지 생성
        image.save("color\\" + str(index-forbid) + "_color.png") # color 폴더에 저장

        # 저장한 사진의 크기가 1000 x 1000 이상이면 big폴더로 옮김
        im = cv2.imread("small\\" + str(index-forbid) + ".jpg")
        h = im.shape[0] # 높이값 저장
        w = im.shape[1] # 너비값 저장
        if w > 1000 and h > 1000:
            shutil.move("small\\" + str(index-forbid) + ".jpg", "big\\" + str(index-forbid) + ".jpg")

        if index == 50: # 무한 크롤링을 방지하기 위해 인덱스가 50이 되면 종료
            break
    except:
        forbid += 1 # 오류 발생시 forbid에 1을 추가하여 jpg 이미지에 숫자 매길때 누락 방지



print("다운로드 완료")

driver.close() # 모든 활동이 끝나서 브라우저 종료

print("by 유한빈")