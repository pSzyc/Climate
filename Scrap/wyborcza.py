from bs4 import BeautifulSoup
import requests
import csv
import os

html_parser = {
    'title': 'art-title',
    'department': 'art-product-name',
    'author': 'art-author',
    'date': 'art-datetime',
    'text': 'art-text'
    }

def get_articles(url):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    articles = soup.find_all(class_='result-item-link',href=True)
    return articles

def get_article_data(link):
    data = {
        'title': None,
        'department': None,
        'author': None,
        'date': None,
        'text': None,
        'link': link
    }
    soup = BeautifulSoup(requests.get(link).text, "html.parser")
    for key, value in html_parser.items():
        try:
            data[key] = soup.find(class_=value).text.replace('\n',"").strip()
        except:
            print(f"Key: {key} not found in {link}")
    return data


csv_file = 'wyborcza.csv'
if not os.path.exists(csv_file):
    print("Creating new csv file " + csv_file)
    column_names = ['Title', 'Department', 'Author', 'Date', 'Text', 'Link']
    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)
else:
    print("Appending to existing csv file " + csv_file)

page = 0
with open('wyborcza.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    while True:
        print(f"Page: {page}")
        link_page = f'https://classic.wyborcza.pl/archiwumGW/0,160510.html?searchForm=&datePeriod=0&initDate=2015-01-01&endDate=2017-01-01&publicationsString=1&author=&page={page}&sort=OLDEST'
        
        data_list = []    
        articles = get_articles(link_page)
        if len(articles) == 0:
            print("No articles found")
            break
        for article in articles:
            link='https://classic.wyborcza.pl/archiwumGW/'+article['href']
            data = get_article_data(link)
            data_list.append(data)
        for data in data_list:
            print(f"{data['title']}/{data['article']}")
            writer.writerow([data['title'], data['department'], data['author'], data['date'], data['text'], data['link']])    
        page += 1