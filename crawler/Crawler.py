import requests
from bs4 import BeautifulSoup

page = 1
lastPage = False

news_url_list = []

while not lastPage:
    url = f"https://news.naver.com/main/list.nhn?mode=LS2D&sid2=259&sid1=101&mid=shm&date=20200906&page={page}"
    print("!@#!@# url : ", url)
    r = requests.get(url)
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

        if type(soup.find("div", {'class':'paging'}).find("a", {'class':'next nclicks(fls.page)'})) == type(None) :
            lastPage = False
        else :
            lp = 0
            for p in soup.find_all("div", {'class':'nclicks(fls.page)'}):
                print("!@#!@# p.text:",p.text)
                if lp < int(p.text):
                    lp = int(p.text)

            if lp == page:
                lastPage = True

        page+=1

    
    
