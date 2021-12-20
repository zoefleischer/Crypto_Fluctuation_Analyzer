import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from textblob import TextBlob
import nltk


# ----------------- WEBSCRAPING------------

# Scraping titles only from www.theinformation.com

def scrapping_pages(x):
    list_text22 = []
    for page in range(1, x):
        url = 'https://www.theinformation.com/topics/crypto/page/' + str(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content)
        news_title = soup.find_all('h3')
        for element in news_title:
            list_text22.append(element.text)
            list_text22 = [element.strip() for element in list_text22]
    return list_text22


titles = scrapping_pages(20)
titles_df = pd.DataFrame(titles)


# Scarping article bodies from www.moneycontrol.com

def get_newsfrompage(x):
    url = 'https://www.moneycontrol.com/news/tags/cryptocurrency.html/page-' + str(x) + '/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    links = soup.find_all('h2')
    titlelist = []
    linklist = []
    fullbody = []
    for link in links[:-1]:
        titlelist.append((link.text))
        linklist.append(link.a['href'])
    for link in linklist:
        response2 = requests.get(link)
        soup2 = BeautifulSoup(response2.content)
        body = soup2.find_all('p')
        fullbody.append(body)

    dict_index = []
    for i in range(0, len(titlelist)):
        dict_index.append({'atitle': titlelist[i], 'blink': linklist[i], 'full news body': str(fullbody[i])})

    return dict_index


articles = get_newsfrompage(3)
articles = pd.DataFrame(articles)


# cleaning tags with regex

def clean_tag(article):
    clean_article = []
    article1 = re.sub('<p>|</p>|<p|<strong>|</strong>', '', article)
    clean_article.append(article1)
    return clean_article


articles['Article'] = articles['full news body'].apply(clean_tag)
articles = articles.drop('full news body', axis=1)
articles.columns = ['Headline', 'Link', 'Article']

# flattening nested list of articles

list1 = list(articles['Article'])
flat_list = []
for sublist in list1:
    for item in sublist:
        flat_list.append(item)
list1 = flat_list

list1 = pd.DataFrame(list1)
list1 = list1.reset_index()
list1.columns = ['index', 'Body']

articles = articles.reset_index()
articles = articles.merge(list1, how='left', on='index')
articles = articles.drop('Article', axis=1)
articles.columns = ['index', 'Headline', 'Link', 'Article']
