from selenium import webdriver
driver = webdriver.Chrome("/Users/seolyumin/chromedriver")
driver.get("https://finance.naver.com/sise/")
print('\n'.join([driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/div[1]/div[2]/ul[1]/li[" + str(i) + "]/a").text for i in range(1, 11)]))
del driver
