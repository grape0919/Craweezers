from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver as wb
import time

# options = wb.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")

driver = wb.Chrome(executable_path='lib/chromedriver.exe')#, chrome_options=options)

news_url_list = []

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
lp = 0
url = f"https://section.blog.naver.com/Search/Post.nhn?pageNo=1&rangeType=ALL&orderBy=sim&keyword=%EB%A1%B1%EB%B0%98%20-%EC%B4%88%EB%A1%B1%EB%B0%98%20-%ED%94%84%EB%9E%AD%ED%81%B4%EB%A6%B0%20-%EC%B9%B4%EC%98%A4%EB%A1%B1%EB%B0%98"
driver.get(url)
driver.find_element_by_xpath("/html/body/ui-view/div/main/div/div/section/div[1]/div[2]/div/div/a").click()
driver.find_element_by_xpath("/html/body/ui-view/div/main/div/div/section/div[1]/div[2]/div/div/div/div/input[1]").clear()
driver.find_element_by_xpath("/html/body/ui-view/div/main/div/div/section/div[1]/div[2]/div/div/div/div/input[1]").send_keys("2018-01-01")
driver.find_element_by_xpath("/html/body/ui-view/div/main/div/div/section/div[1]/div[2]/div/div/div/div/input[2]").clear()
driver.find_element_by_xpath("/html/body/ui-view/div/main/div/div/section/div[1]/div[2]/div/div/div/div/input[2]").send_keys("2020-09-08")
driver.find_element_by_xpath("/html/body/ui-view/div/main/div/div/section/div[1]/div[2]/div/div/div/div/a").click()

#상세검색 제외 단어 추가
# driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div[1]/div/form[8]/fieldset/a").click()
# driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div[1]/div/form[8]/fieldset/div/div[2]/input").send_keys("초롱반")
# driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div[1]/div/form[8]/fieldset/div/div[5]/input").click()


urls = []
lastPage = False
pages = []
page = 1
while not lastPage:

    driver.get(f"https://section.blog.naver.com/Search/Post.nhn?pageNo={page}&rangeType=ALL&orderBy=sim&keyword=%EB%A1%B1%EB%B0%98%20-%EC%B4%88%EB%A1%B1%EB%B0%98%20-%ED%94%84%EB%9E%AD%ED%81%B4%EB%A6%B0%20-%EC%B9%B4%EC%98%A4%EB%A1%B1%EB%B0%98")
    
    elements = []
    time.sleep(1)
    element = driver.find_element_by_class_name("area_list_search")
    elements = element.find_elements_by_class_name("desc_inner")

    for e in elements:
        urls.append(e.get_attribute("href"))

    soup = bs(driver.page_source, 'html.parser')
    temp = soup.find("a", {'class':'button_next'})
    if temp == None:
        # TODO : 마지막 페이지 번호 추출
        paginationEle = driver.find_element_by_class_name("pagination")
        pagiEles = paginationEle.find_element_by_class_name("item")
        lp = 0 
        for e in pagiEles:
            if lp < int(e.text):
                lp = int(e.text)
    
        if page == lp:
            lastPage = True

    page += 1

print("url length : ", len(urls))


time.sleep(10)
# while not lastPage:
#     print("!@#!@# url : ", url)

#     soup = BeautifulSoup(driver.page_source, 'html.parser')