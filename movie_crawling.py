import requests
from bs4 import BeautifulSoup
from urllib import parse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time 

url_login = 'https://nid.naver.com/nidlogin.login'
id = ' ' #네이버 아이디 입력
pw = ' ' #네이버 비번 입력

driver = webdriver.Chrome(r'C:\chromedriver.exe') #크롬드라이버 위치 입력
driver.get(url_login)
driver.implicitly_wait(2)

# execute_script 함수 사용하여 자바스크립트로 id,pw 넘겨주기
driver.execute_script("document.getElementsByName('id')[0].value=\'"+id+"\'")
driver.execute_script("document.getElementsByName('pw')[0].value=\'"+pw+"\'")

# 로그인 버튼 클릭하기
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
time.sleep(1)

base_url='https://serieson.naver.com/movie/categoryList.nhn?categoryCode=100005&orderType=sale&sortingType=&mobileYn=&drmFreeYn=&freeYn=&discountYn=&tagCode=1'


comment_list=[]
for page in range(1,10):
    url=base_url.format(1)
    res=requests.get(url)
    if res.status_code ==200:
        soup=BeautifulSoup(res.text,'lxml')
        tds=soup.select('div.c_bg>li>div>h3,title') #여기가 잘못 된 것 같아요
        print(len(tds))
        for td in tds:
            try:
                movie_title=td.select_one('a.movie').text.strip()
                score=td.select_one('div.c_bg_score>em').text.strip() #여기랑요
                comment=td.select_one('br').next_sibling.strip()
            
                comment_list.append((movie_title, score))
                time.sleep(0.5)
            except Exception as e:
                continue
print('end')

import pandas as pd
df=pd.DataFrame(comment_list, columns=['영화제목','평점']) #오류 해결하고 줄거리도 추가할 예정입니다
df.to_csv('navercommenttt.csv', encoding='utf-8',index=False)