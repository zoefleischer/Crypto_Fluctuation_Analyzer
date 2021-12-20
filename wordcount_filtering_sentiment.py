import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from textblob import TextBlob
import nltk



# ---------------- POST PROCESSING-----------

# Count occurence of words in nouns

def word_count(list):
    counts = dict()
    coinlist = ['bitcoin', 'ethereum', 'yearn.finance', 'tether', 'ripple', 'btc', 'etc', 'yfi', 'usdt', 'xrp']
    for word in list.lower().split(' '):
        if word in coinlist:
            if word in counts:
                counts[word] += 1
            else:
                counts[word] = 1
        else:
            pass
    return counts


# run word_count for each article

new_list = []
for article in list1:
    counts = word_count(article)
    new_list.append(counts)
    print(new_list)

new_list = pd.DataFrame(new_list)

articles = articles.reset_index()
new_list = new_list.reset_index()
coins_articles = articles.merge(new_list, how='left', on='index')

# --------------------------------FILTERING---------------------------

coins_articles = coins_articles.fillna()
condition = coins_articles['bitcoin'] > 3 or coins_articles['btc'] > 3
bitcoin = coins_articles[condition]

# ---------------------------------- SENTIMENT ----------------------------

articles1 = bitcoin['Article']
articles1 = list(articles1)

sentiments = []
for article in articles1:
    article = TextBlob(article)
    sentiments.append(article.sentiment)
    print(sentiments)

sentiments_df = pd.DataFrame(sentiments)

# ----------------------MERGE INTO ONE DATAFRAME----------------------

bitcoin = bitcoin.reset_index()
bitcoin = bitcoin.drop('level_0', axis=1)
bitcoin = bitcoin.drop('index', axis=1)
bitcoin = bitcoin.reset_index()

sentiments_df = sentiments_df.reset_index()

bitcoin_sentiments = bitcoin.merge(sentiments_df, how='left', on='index')
bitcoin_sentiments