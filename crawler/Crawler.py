from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver as wb

options = wb.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = wb.Chrome(executable_path='lib/chromedriver.exe', chrome_options=options)

page = 1
lastPage = False

news_url_list = []

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
lp = 0
while not lastPage:
    url = f"https://news.naver.com/main/list.nhn?mode=LS2D&sid2=259&sid1=101&mid=shm&date=20200906&page={page}"
    print("!@#!@# url : ", url)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    news1 = soup.find("ul", {'class':'type06_headline'})
    for f in news1.find_all("a"):
        news_url_list.append(f['href'])

    news2 = soup.find("ul", {'class':'type06'})
    for f in news1.find_all("a"):
        news_url_list.append(f['href'])

    temp = soup.find("div", {'class':'paging'}).find("a", {'class':'next nclicks(fls.page)'})
    print("!@#!@# temp : " , temp)
    if type(temp) == type(None) :
        for p in soup.find_all("a", {'class':'nclicks(fls.page)'}):
            print("!@#!@# p.text:",p.text)
            if lp < int(p.text):
                lp = int(p.text)
        
        print("!@#!@# lp : ", lp)
        if lp == page:
            lastPage = True
        else:
            lastPage = False
    else :
        lastPage = False

    page+=1



datas = []

for u in news_url_list:
    driver.get(u)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print("error soup : ", soup)
    title = soup.find("h3", {'class':'tts_head'}).get_text().replace("\n"," ")
    pub_date = soup.find("span", {'class':'t11'}).get_text().replace("\n"," ")
    content = soup.find("div", {'id':'articleBodyContents'}).get_text().replace("\n"," ")

    news_pair = (title, content, pub_date, u)
    datas.append(news_pair)

df = pd.DataFrame(datas)
df.to_csv("./test.csv",sep="|",na_rep='NaN', encoding='utf-8')
