from selenium import webdriver

keyword_list = []
user_keyword = input('원하시는 키워드를 입력하세요.')

while user_keyword != '':

    driver = webdriver.Chrome('C:\\Users\\chromedriver')
    url = "https://m.some.co.kr/analysis/keyword"
    driver.get(url)

    # 검색창에 키워드 입력
    search_box = driver.find_element_by_xpath('/html/body/div[2]/div[1]/section/div/div/section[1]/div/input')
    search_box.send_keys(user_keyword)

    # 검색버튼 클릭
    click_box = driver.find_element_by_xpath('/html/body/div[2]/div[1]/section/div/div/section[3]/a')
    click_box.click()

    # 웹페이지 요소 생성 대기시간
    driver.implicitly_wait(10)

    rel_search = []

    table = driver.find_element_by_xpath('/html/body/div[2]/section[2]/div/div/section/div[2]/div[2]/div[3]/div/div/div[5]/div/div/div/div/table/tbody')

    for tr in table.find_elements_by_tag_name('tr'):
        td = tr.find_elements_by_tag_name('td')
        rel_search.append(td[1].text + ' - ' + td[2].text)

    print('입력하신 키워드의 연관 검색어입니다.')
    for keyword in rel_search:
        print(keyword)

    driver.quit()

    add_keyword = input('현재 검색어를 키워드로 등록하시겠습니까?(y/n)')

    if add_keyword == 'y':
        keyword_list.append(user_keyword)

    user_keyword = input('계속 검색하시려면 키워드를 입력해주세요.') # 추가 키워드 입력 없을 시 종료

print(keyword_list)