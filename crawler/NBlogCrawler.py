from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver as wb

from selenium.webdriver.support import expected_conditions as EC
import time
import requests
# options = wb.ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")

driver = wb.Chrome(executable_path='lib/chromedriver.exe')#, chrome_options=options)
driver.implicitly_wait(10)
news_url_list = []

driver.implicitly_wait(10)
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
lp = 0
url = f"https://section.blog.naver.com/Search/Post.nhn?pageNo=1&rangeType=ALL&orderBy=sim&keyword=%EB%A1%B1%EB%B0%98%20-%EC%B4%88%EB%A1%B1%EB%B0%98%20-%ED%94%84%EB%9E%AD%ED%81%B4%EB%A6%B0%20-%EC%B9%B4%EC%98%A4%EB%A1%B1%EB%B0%98"
driver.get(url)
driver.find_element_by_class_name("present_selected").click()
driver.find_element_by_id("search_start_date").clear()
driver.find_element_by_id("search_start_date").send_keys("2018-01-01")
driver.find_element_by_id("search_end_date").clear()
driver.find_element_by_id("search_end_date").send_keys("2020-09-08")
driver.find_element_by_id("periodSearch").click()

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
    element = driver.find_element_by_class_name("area_list_search")
    elements = element.find_elements_by_class_name("desc_inner")

    for e in elements:
        urls.append(e.get_attribute("href"))

    print("!@#!@# urls : ", len(urls))
    soup = bs(driver.page_source, 'html.parser')
    temp = soup.find("a", {'class':'button_next'})
    if temp == None:
        # TODO : 마지막 페이지 번호 추출
        paginationEle = driver.find_element_by_class_name("pagination")
        pagiEles = paginationEle.find_elements_by_class_name("item")
        lp = 0 
        for e in pagiEles:
            if lp < int(e.text):
                lp = int(e.text)
    
        if page == lp:
            lastPage = True

    page += 1

print("!@#!@# result url length : ", len(urls))  # 1475

f = open("./urls.txt", "w")
for u in urls:
    f.write(u+"\n")

    # request = requests.get(u)
    # html = request.text
    # print("html : ", html)
    # driver.get(u)
    # titleEl = driver.find_element_by_class_name("se-component-content").find_element_by_class_name("pcol1").text
    # if titleEl == None:
    #     titleEl = driver.find_element_by_class_name("itemSubjectBoldfont")
    
    # title = titleEl.text
    # conts = driver.find_element_by_class_name()
    
    # dateEl = driver.find_element_by_class_name("se_publishDate")
    # if dateEl == None:
    #     dateEl = driver.find_element_by_class_name("_postAddDate")
    # pub_date = dateEl.text

f.close()


def readAndParsing():
    print("")
    for r in f.open("").read:
        driver.get(u)

        try:
            titleEl = driver.find_element_by_class_name("se-title-text")
        except:
            try:
                titleEl = driver.find_element_by_class_name("se_title")
            except:
                print("!@#!@# skip url : ", u)
                continue

        title = titleEl.text

        conts = driver.find_element_by_class_name("__se_component_area")
        id = postViewArea
        try:
            dateEl = driver.find_element_by_class_name("se_publishDate")
        except:
            try:
                dateEl = driver.find_element_by_class_name("_postAddDate")
            except:
                
                print("!@#!@# skip url : ", u)
                continue

        pub_date = dateEl.text

        blogContent = (title, conts, pub_date)

        crawedDataList.append(blogContent)


    df = pd.DataFrame(crawedDataList)
    df.to_csv("./test.csv",sep="|",na_rep='NaN')