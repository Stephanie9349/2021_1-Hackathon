from selenium import webdriver
import time

keep_searching = 'y'
while keep_searching != '':

    user_keyword = input('원하시는 키워드를 입력하세요.')

    driver = webdriver.Chrome('/Users/seolyumin/chromedriver')
    url = "https://m.some.co.kr/analysis/keyword"
    driver.get(url)

    search_box = driver.find_element_by_xpath('/html/body/div[2]/div[1]/section/div/div/section[1]/div/input')
    search_box.send_keys(user_keyword)

    click_box = driver.find_element_by_xpath('/html/body/div[2]/div[1]/section/div/div/section[3]/a')
    click_box.click()

    time.sleep(3)

    rel_search = []

    table = driver.find_element_by_xpath(
        '/html/body/div[2]/section[2]/div/div/section/div[2]/div[2]/div[3]/div/div/div[5]/div/div/div/div/table/tbody')

    for tr in table.find_elements_by_tag_name('tr'):
        td = tr.find_elements_by_tag_name('td')
        rel_search.append(td[1].text + '-' + td[2].text)

    with open('collected_keywords.txt', 'w') as f:
        f.write('2021년 6월 4주차 연관검색어 순위\n')

    for i, value in enumerate(rel_search):
        with open('collected_keywords.txt', 'a') as f:
            f.write('{}. {}\n'.format(i + 1, value))

    driver.quit()

    keep_searching = input('계속 검색하시려면 키워드를 입력해주세요.')