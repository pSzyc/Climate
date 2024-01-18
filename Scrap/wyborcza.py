#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import csv
import os
from selenium import webdriver
from tqdm import tqdm
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--headless")
chrome_options.add_argument("user-data-dir=selenium")
driver = webdriver.Chrome(options=chrome_options)

html_parser = {
    'title': 'art-title',
    'department': 'art-product-name',
    'author': 'art-author',
    'date': 'art-datetime',
    'text': 'art_paragraph'
    }

def list_articles(url):
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
    driver.get(link)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    for key, value in html_parser.items():
        try:
            if key == 'text':
                paragraphs = soup.find_all(class_=value)
                data[key] = " ".join([paragraph.text for  paragraph in paragraphs]).replace('\n',"").strip()
            else:
                data[key] = soup.find(class_=value).text.replace('\n',"").strip()
        except:
            pass
    return data

def process_page(link_page):
    data_list = []    
    articles = list_articles(link_page)
    for article in articles:
        link='https://classic.wyborcza.pl/archiwumGW/'+article['href']
        data = get_article_data(link)
        data_list.append(data)
    return data_list

csv_file = 'wyborcza.csv'
if not os.path.exists(csv_file):
    print(f"Creating file {csv_file}")
    column_names = ['Title', 'Department', 'Author', 'Date', 'Text', 'Link']
    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)
else:
    print(f"Appending to {csv_file}")

with open(csv_file, 'a', newline='') as file:
    writer = csv.writer(file)
    for page in tqdm(range(10223)):
        link_page = f'https://classic.wyborcza.pl/archiwumGW/0,160510.html?searchForm=&datePeriod=0&initDate=2019-01-01&endDate=2023-01-01&publicationsString=1%3B5&author=&page={page}&sort=OLDEST'
        data_list = process_page(link_page)
        for data in data_list:
            writer.writerow([data['title'], data['department'], data['author'], data['date'], data['text'], data['link']])    