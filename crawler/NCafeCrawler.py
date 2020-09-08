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
url = f"https://section.cafe.naver.com/cafe-home/search/articles?query=%EB%A1%B1%EB%B0%98#%7B%22query%22%3A%22%EB%A1%B1%EB%B0%98%22%2C%22page%22%3A1%2C%22sortBy%22%3A0%2C%22period%22%3A%5B%222003.12.01%22%2C%222020.09.08%22%5D%2C%22menuType%22%3A%5B0%5D%2C%22searchBy%22%3A0%2C%22duplicate%22%3Afalse%2C%22includeAll%22%3A%22%22%2C%22exclude%22%3A%22%22%2C%22include%22%3A%22%22%2C%22exact%22%3A%22%22%7D"
driver.get(url)
driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div[1]/div/form[2]/fieldset/div/div[1]/div[2]/a").click()
driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div[1]/div/form[2]/fieldset/div/div[2]/div[1]/input[1]").clear()
driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div[1]/div/form[2]/fieldset/div/div[2]/div[1]/input[1]").send_keys("2018.01.01")
# driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div[1]/div/form[2]/fieldset/div/div[2]/div[1]/input[2]").send_keys("2020.09.08")
driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div[1]/div/form[2]/fieldset/div/div[2]/div[2]/input").click()

#상세검색 제외 단어 추가
driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div[1]/div/form[8]/fieldset/a").click()
driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div[1]/div/form[8]/fieldset/div/div[2]/input").send_keys("초롱반")
driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div[1]/div/form[8]/fieldset/div/div[5]/input").click()


# print(element.get_atrribute("outerHTML"))

urls = []
lastPage = False
pages = []
while not lastPage:

    for i in range(1,11):
        pageElement = driver.find_element_by_xpath(f"/html/body/div[2]/div[2]/div/div[2]/div[2]/div/div[3]/div[2]/button[{i}]")
        if pageElement == None:
            lastPage = True
            break
        elif pageElement.text in pages:
            continue
        else :
            pageElement.click()
            elements = []
            
            element = driver.find_element_by_id("ArticleSearchResultArea")
            elements = element.find_elements_by_class_name("_ellipsisArticleTitle")

            for e in elements:
                urls.append(e.get_attribute("href"))

    if not lastPage:
        nextElement = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[2]/div[2]/div/div[3]/div[2]/button[11]")
        if nextElement == None:
            lastPage = True
        else :
            nextElement.click()

print("url length : ", len(urls))


time.sleep(10)
# while not lastPage:
#     print("!@#!@# url : ", url)

#     soup = BeautifulSoup(driver.page_source, 'html.parser')