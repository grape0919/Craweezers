import requests
from bs4 import BeautifulSoup
import pandas as pd

page = 1
lastPage = False

news_url_list = []

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
lp = 0
while not lastPage:
    url = f"https://news.naver.com/main/list.nhn?mode=LS2D&sid2=259&sid1=101&mid=shm&date=20200906&page={page}"
    print("!@#!@# url : ", url)
    r = requests.get(url,headers=headers)
    print("!@#!@# status_code : " + str(r.status_code))

    if r.status_code == 200:

        soup = BeautifulSoup(r.text, 'html.parser')
        # print("!@#!@# result : ",soup.text)

        news1 = soup.find("ul", {'class':'type06_headline'})
        # print("!@#!@# news1", news1)
        for f in news1.find_all("a"):
            news_url_list.append(f['href'])

        news2 = soup.find("ul", {'class':'type06'})
        # print("!@#!@# news2", news2)
        for f in news1.find_all("a"):
            news_url_list.append(f['href'])

        # print("!@#!@# new LIST : ", news_url_list)
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

    print("!@#!@# lastPage:", lastPage)


datas = []

for u in news_url_list:
    r = requests.get(u,headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find("h3", {'class':'articleTitle'})
    pub_date = soup.find("span", {'class':'t11'})
    content = soup.find("div", {'id':'articleBodyContents'})

    news_pair = (title, content, pub_date, u)
    datas.append(news_pair)

df = pd.DataFrame(datas)
df.to_csv("./test.csv",sep=",",na_rep='NaN', encoding='utf-8')
# ,columns=['TITLE', 'COTENT', 'PUB_DATE', 'URL'])
