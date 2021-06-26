import pandas as pd
from selenium import webdriver
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
    id = ''  # 네이버 아이디 입력
    pw = ''  # 네이버 비번 입력

    driver = webdriver.Chrome('/Users/seolyumin/chromedriver')  # 크롬드라이버 위치 입력
    driver.get(url_login)
    driver.implicitly_wait(2)

    # execute_script 함수 사용하여 자바스크립트로 id,pw 넘겨주기
    driver.execute_script("document.getElementsByName('id')[0].value=\'" + id + "\'")
    driver.execute_script("document.getElementsByName('pw')[0].value=\'" + pw + "\'")

    # 로그인 버튼 클릭하기
    driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
    time.sleep(1)

    # 브라우저 등록 / 등록 안 함
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/form/fieldset/span[2]/a').click()
    time.sleep(1)

    base_url = 'https://serieson.naver.com/movie/categoryList.nhn?categoryCode=100005&orderType=sale&sortingType=&mobileYn=&drmFreeYn=&freeYn=&discountYn=&tagCode=1&page={}'

    comment_list = []
    for page in range(1, 2):
        url = base_url.format(page)
        driver.get(url)
        time.sleep(3)
        for ul in range(1, 6):
            for li in range(1, 6):
                driver.find_element_by_xpath(
                    "/html/body/div[2]/div[2]/div[2]/div/ul[" + str(ul) + "]/li[" + str(li) + "]/a").click()
                title = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/h2").text
                rate = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[1]/div[1]/em").text
                plot = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[4]").text
                comment_list.append([title.replace("HD(1080) 19 ", "").replace("HD(1080) ", "").replace("19 ", ""), rate, plot])
                driver.back()
                time.sleep(1)

    df = pd.DataFrame(comment_list, columns=['title', 'rate', 'plot'])  # 오류 해결하고 줄거리도 추가할 예정입니다
    df.to_csv('navercommenttt.csv', encoding='utf-8', index=False)
    file1 = pd.read_csv('navercommenttt.csv')
    print(file1)
    

def recommendation(keywords):
    list_flag = [0 for i in range(len(keywords))]
    flag_num = [0 for i in range(len(keywords))]
    file1 = pd.read_csv("/Users/seolyumin/Hackathon-selenium/navercommenttt.csv", header=None, names=["title", "rate", "plot"])
    title = list(file1['title'])
    rate = list(file1['rate'])
    plot = list(file1['plot'])
    priority = [0 for i in range(len(title))]
    priority_index = [0 for i in range(len(priority))]
    for k in keywords:
        for i in plot:
            if k in str(i):
                list_flag[keywords.index(k)] = 1
                priority[plot.index(i)] += 1

    flag_num = priority[:]

    for i in range(len(priority)):
        priority_index[i] = priority.index(max(priority))
        priority[priority.index(max(priority))] = -1

    for i in range(len(priority_index)):
        if flag_num[priority_index[i]] > 0:
            print(title[priority_index[i]], "# 키워드", flag_num[priority_index[i]], "개 포함 |", "당신과의 찰떡 지수:", round(flag_num[priority_index[i]] / len(keywords) * 100, 1), "%")

#movie_crawling()            

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
[print(word, end=' ') for word in derived_keywords]
print()
print("**********************************")
keywords2 = list(map(str, input().split()))
for word in keywords2:
    word.replace("\x7f", "")
selected_keywords.extend(keywords2)

recommendation(selected_keywords)