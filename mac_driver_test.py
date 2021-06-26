# 맥 크롬드라이버 경로가 달라 테스트하는 용도로 만든 파일입니다.
# 수정사항이 있을 경우 원본에서 수정해주세요!

import pandas as pd
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from urllib import parse
from selenium.webdriver.common.keys import Keys 
import time 

def keyword_crawling(keyword): # 테스트를 위한 간소화 상태
    rel_search = []
    user_keyword = keyword

    driver = webdriver.Chrome('/Users/seolyumin/chromedriver')
    url = "https://m.some.co.kr/analysis/keyword"
    driver.get(url)

    search_box = driver.find_element_by_xpath('/html/body/div[2]/div[1]/section/div/div/section[1]/div/input')
    search_box.send_keys(user_keyword)

    click_box = driver.find_element_by_xpath('/html/body/div[2]/div[1]/section/div/div/section[3]/a')
    click_box.click()

    time.sleep(3)

    table = driver.find_element_by_xpath('/html/body/div[2]/section[2]/div/div/section/div[2]/div[2]/div[3]/div/div/div[5]/div/div/div/div/table/tbody')

    for tr in table.find_elements_by_tag_name('tr'):
        td = tr.find_elements_by_tag_name('td')
        rel_search.append(td[1].text)

    driver.quit()

    return rel_search

def movie_crawling():
    url_login = 'https://nid.naver.com/nidlogin.login'
    id = ' ' #네이버 아이디 입력
    pw = ' ' #네이버 비번 입력

    driver = webdriver.Chrome('/Users/seolyumin/chromedriver') #크롬드라이버 위치 입력
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

def recommendation(keywords):
    list_flag = [0 for i in range(len(keywords))]
    flag_num = [0 for i in range(len(keywords))]
    file1 = pd.read_csv("/Users/seolyumin/Hackathon-selenium/csv_test2.csv", header=None, names=["title", "rate", "plot"])
    title = list(file1['title'])
    rate = list(file1['rate'])
    plot = list(file1['plot'])
    priority = [0 for i in range(len(title))]
    priority_index = [0 for i in range(len(priority))]
    # print(title)
    # print(rate)
    # print(plot)
    for k in keywords:
        for i in plot:
            if k in i:
                list_flag[keywords.index(k)] = 1
                priority[plot.index(i)] += 1

    flag_num = priority[:]

    for i in range(len(priority)):
        priority_index[i] = priority.index(max(priority))
        priority[priority.index(max(priority))] = -1

    for i in range(len(priority_index)):
        if flag_num[priority_index[i]] > 0:
            print(title[priority_index[i]], "# 키워드", flag_num[priority_index[i]], "개 포함 |", "당신과의 찰떡 지수:", flag_num[priority_index[i]] / len(keywords) * 100, "%")
            

derived_keywords = []
selected_keywords = []

print("키워드를 선택해주세요: ")
print("범죄 / 자연재해 / 괴물 / 오컬트") # 키워드 수정 바람
keywords1 = list(map(str, input().split()))
selected_keywords.extend(keywords1)

for word in keywords1:
    derived_keywords.extend(keyword_crawling(word))

print("세부 키워드를 선택해주세요: ")
print("**********************************")
print()
[print(word, end=' ') for word in derived_keywords]
print()
print("**********************************")
keywords2 = list(map(str, input().split()))
selected_keywords.extend(keywords2)

recommendation(selected_keywords)

