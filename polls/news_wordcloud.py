import time
import random
from bs4 import BeautifulSoup
import requests
import pandas as pd
from konlpy.tag import Hannanum
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
number = 1

def wordcloud(url):
    global word_list
    hannanum = Hannanum()

    contents = []
    request = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
    html = request.text

    f = open("polls/news.txt", 'w')
    f.write(html)
    f.close()



def collect_and_store(keyword):
    news_detail = []

    url = "https://search.naver.com/search.naver?where=news&query=" + keyword
       
       
    while True:
        req = requests.get(url, headers = header)
        cont = req.content
        soup = BeautifulSoup(cont, 'html.parser')

        naver_news = soup.find_all("a", {"class":"info"})
        if naver_news == []:
            break

            get
       
        for a_tag in naver_news[0:3]:
            try:
                news_url = a_tag.attrs["href"]
                if news_url.startswith("https://n.news.naver.com"):
                    wordcloud(news_url)
                   
                   
            except Exception as e:
                print(e)
                continue
        break