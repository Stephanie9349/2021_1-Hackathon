from bs4 import BeautifulSoup
import requests 
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys 
import time 
import re 
import pandas as pd

url_login = 'https://nid.naver.com/nidlogin.login'
id = '' #네이버 아이디 입력
pw = '' #네이버 비번 입력

driver = wd.Chrome(r'C:\chromedriver.exe') #크롬드라이버 위치 넣기
driver.get(url_login)
driver.implicitly_wait(2)

# execute_script 함수 사용하여 자바스크립트로 id,pw 넘겨주기
driver.execute_script("document.getElementsByName('id')[0].value=\'"+id+"\'")
driver.execute_script("document.getElementsByName('pw')[0].value=\'"+pw+"\'")

# 로그인 버튼 클릭하기
driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
time.sleep(1)

def getPageLinks(pageRange):
    global links
    links = [] 
    
    for pageNo in range(pageRange): 
        url = "https://serieson.naver.com/movie/categoryList.nhn?categoryCode=100005&orderType=sale&sortingType=&mobileYn=&drmFreeYn=&freeYn=&discountYn=&tagCode=1&page=" + str(pageNo + 1) 
        req=requests.get(url) 
        soup = BeautifulSoup(req.text, 'lxml') 
        movielinks = soup.select('div.lst_thum_wrap ul li a[href]') 
        
        for movielink in movielinks:
            link = str(movielink.get('href'))
            links.append("https://series.naver.com"+link)
    

getPageLinks(5) #원하는 페이지 수 넣기


title_infos = []
content_infos = []
score_infos = []
    
url2 = "https://www.naver.com" 

driver = wd.Chrome(executable_path=r'C:\chromedriver.exe') 
driver.get(url2) 
time.sleep(2.0)  
    
driver.find_element_by_css_selector('body').send_keys(Keys.CONTROL + "t") 
    
for link in links:
        driver.switch_to.window(driver.window_handles[-1]) 
        time.sleep(0.1) 
        driver.get(link) 
        time.sleep(0.1) 
        driver.switch_to.window(driver.window_handles[0]) 
        time.sleep(0.3) 
        
        html_source = driver.page_source 
        
        html_soup = BeautifulSoup(html_source, 'lxml') 
        
        flag = html_soup.text[0:10] 
        
        newflag = "".join(flag) 
        newflag = newflag.replace('\n', '') 
        
        if newflag == '네이버':
            time.sleep(1.0) 
            
            score = driver.find_element_by_css_selector('div.score_area > em') 
            
            score = float(score.text) 
            score = int(score) 
            score_infos.append(score) 
            
            text = driver.find_element_by_css_selector('div.end_head.NE\=a\:mvi > h2') #의문1
            
            movieInfoUrl = text.get_attribute('href') 
            movie_req = requests.get(movieInfoUrl) 
            movie_soup = BeautifulSoup(movie_req.text, 'lxml') 
            titles = movie_soup.select('div.mv_info > h3.h_movie > a') #의문2
            temp_titles = [] 
            
            for title in titles:
                temp = title.text 
                temp = temp.replace('상영중', '') 
                temp = temp.replace('\n', '') 
                temp_titles.append(temp) 
                
            if '' in temp_titles or ' ' in temp_titles:
                temp_titles.remove('') 
                
            temp_titles = set(temp_titles) 
            temp_titles = list(temp_titles) 
            temp_titles = [x for x in temp_titles if x != ''] 
            title_infos.append(list(temp_titles)[0]) 
            
            contents_texts = movie_soup.select('div.story_area > p.con_tx') #의문3
            
            if len(contents_texts) == 0:
                content_infos.append("줄거리 오류") 
            else:
                for contents in contents_texts:
                    temp = contents.text 
                    temp = temp.replace('\r', '') 
                    temp = temp.replace('\xa0', '') 
                    content_infos.append(temp) 
                
print(len(score_infos), len(content_infos)) 
    
driver.close() 
    
movie_dic = {"평점":score_infos, "줄거리":content_infos} 
movie_df = pd.DataFrame(movie_dic, index=title_infos) 
movie_df2 = movie_df.drop_duplicates("줄거리", keep='first') 
    

try: 
    movie_df.to_csv(('movie_data.csv'), sep=',', na_rep='NaN', encoding='euc-kr') 
except: 
        print("Error")