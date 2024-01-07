from bs4 import BeautifulSoup
import os
import requests
from selenium import webdriver
#import chromedriver_binary
#from time import sleep
import pandas as pd
#from PyPDF2 import PdfReader
#from io import BytesIO
#import openpyxl

from selenium.webdriver.common.by import By


def download_pdf():
    options = webdriver.ChromeOptions()
    options.add_argument(r'--user-data-dir=C:\Users\Lis\AppData\Local\Google\Chrome\User Data\ ')
    PATH = r".\venv\Lib\site-packages\chromedriver_binary\chromedriver.exe"
    driver = webdriver.Chrome(PATH, options=options)
    last_page=pd.read_csv("wyborcza.csv")['page'].tail(1).iloc[0]
    #last_keyword=pd.read_csv("wyborcza.csv")['title']

    source = "wyborcza.pl"
    #driver = webdriver.Chrome()

    input()
    #with open('keywords.txt') as f:
    #     keyword_list= f.readlines()
    #keyword_list=str(keyword_list[0]).split(",")
    #copylist=keyword_list.copy()
   # print(copylist)



    #for keyword in keyword_list:
    url = f'https://classic.wyborcza.pl/archiwumGW/0,160510.html?searchForm=&datePeriod=0&initDate=2017-05-15&endDate=2022-12-31&publicationsString=1%3B5&author=&page=0&sort=OLDEST'
    total_articles=0
       # keywordList = [["Klucz:" + keyword, -1, "", "", "", "", "", ""]]
       # excel(keywordList)
    while True:

        title = "None"
        dzial = "None"
        author = "None"
        date = "None"
        text = "None"
        lead = ""


        requests.get(url)
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        current_page=url[url.find("page=")+len("page="):url.find('&sort')]
        print(last_page)
        print(current_page)
        #current_page=current_page.find('span').text
        print("Current Page: " ,current_page)

        url=url.replace("page="+str(current_page),"page="+str(int(current_page)+1))
        print(current_page)


        if int(last_page) < int(current_page):
            #url = "http://archiwum.rp.pl" + soup.find( class_="next")['href']

            articles = soup.find_all(class_='result-item-link',href=True)
            mg=1
            articles_list = []
            print(articles)
            if not articles:
                break
            for article in articles:
                link='https://classic.wyborcza.pl/archiwumGW/'+article['href']
                driver.get(link)


                soup = BeautifulSoup(driver.page_source, "html.parser")
                try:
                    title=soup.find(class_='art-title').text.replace('\n',"")
                    print("Article: ", mg, "/", len(articles),"     ",title)


                except AttributeError:
                    print("Title Error")
                    pass
                try:
                    dzial = soup.find(class_='art-product-name').text.replace('\n', "").replace(" ", "")

                except AttributeError:
                    print("dzial Error")
                    pass
                try:
                    author=soup.find(class_='art-author').text.replace('\n',"")

                except AttributeError:
                    print("author Error")
                    pass
                try:
                    date=soup.find(class_='art-datetime').text

                except AttributeError:
                    print("date Error")
                    pass
                try:
                    text=soup.find(class_='article-text').text.replace('\n',"")

                except AttributeError:
                    print("text Error")
                    pass
                try:
                    lead=soup.find(class_='article-lead').text.replace('\n',"")

                except AttributeError:
                    print("lead Error")
                    pass
                author=author.replace("WŁADIMIR PUTIN*","None").replace("ROZMAWIAŁA","").replace("ROZMAWIAŁ","")
                articles_list.append([title, current_page,lead+text, link, source, author, dzial,  date])



                mg += 1
                total_articles+=1
            print(total_articles)
            excel(articles_list)

        #new_section_excel(keyword)
        #current_page = +1
       # with open('keywords.txt', 'w') as file:
            #copylist.remove(keyword)
            #file.writelines(copylist)
       # file.close()

    driver.quit()



def excel(article):
    print("EXCEL ACTIVATION")
    id=[]
    last_id=int(pd.read_csv("wyborcza.csv")['id'].tail(1).iloc[0])+1
    #print("last id ", last_id)
    for i in range(last_id,last_id+len(article)):
        #print(i)
        id.append(i)

    df = pd.DataFrame(article,index=id,
                    columns=['title', 'page', 'text', 'link', 'source', 'author','department', 'date'])
    df.to_csv('wyborcza.csv',mode='a', index=True ,header=False)
    return
#pd.read_csv("Gazeta.csv")['id'].tail(1).iloc[0]

if __name__ == '__main__':
    download_pdf()
    # excel()
