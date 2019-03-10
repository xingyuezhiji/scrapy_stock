
#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/1 22:09
# @Author  : xingyuezhiji
# @Email   : zhong180@126.com
# @File    : Spider_news.py
# @Software: PyCharm Community Edition
#coding=utf-8


import re
from urllib import request
import socket
from bs4 import BeautifulSoup as bs
# import pandas as pd

import requests

from pymongo import MongoClient
import datetime
# client = MongoClient('localhost',27017)
client = MongoClient('10.249.180.192:8000', 27017)
db = client.stock
data = db.data
news = db.news
# news = db.news

# 爬取新闻
def parse_news(url):
    # title1 = title
    socket.setdefaulttimeout(200)
    headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}
    # req = request.Request(quote(url,safe='/:?='), headers=headers)
    # response = request.urlopen(req)
    response = requests.get(url, headers=headers)
    # response = requests.get(quote(url, safe='/:?='), headers=headers)

    # print(response.encoding)
    try:
        html_data = response.text.encode(response.encoding)
    except:
        html_data = response.text

    # print(html_data)
    soup = bs(html_data, 'lxml',from_encoding='utf-8')

    contents = soup.find_all(class_='common_box')
    # title = soup.find_next(class_='common_box')
    # print(contents[2].find('p').get_text())
    content = contents[2].find('p').get_text()
    return content




# 爬取新闻网址
def parse(code):
    socket.setdefaulttimeout(200)
    url = 'http://www.aastocks.com/sc/stocks/analysis/stock-aafn/{}/0/hk-stock-news/1'.format(code)
    headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}

    # req = request.Request(quote(url,safe='/:?='), headers=headers)
    # response = request.urlopen(req)
    response = requests.get(url, headers=headers)
    # print(response.encoding)
    try:
        html_data = response.text.encode(response.encoding) #utf-8
    except:
        html_data = response.text
    soup = bs(html_data, 'html.parser', from_encoding='utf-8')
    # print(soup)
    url_list = []
    date_list = []
    title_list =[]
    results = soup.find(id='aafn-search-c1').find_all('div',attrs={'ref':re.compile(r'NOW?')})
    for result in results:
        try:
            link = result.find("a")['href']
            title = result.find("a")['title']
            date = result.find(class_='newstime4')
            link = 'http://www.aastocks.com'+link
        except:
            continue
        # print(title)
        # print(link)
        # print(date.get_text())
        url_list.append(link)
        date_list.append(date.get_text())
        title_list.append(title)

    return url_list,date_list,title_list



def Crawl(code):
    parse_datas_list = []
    url_list, date_list, title_list= parse(code)
    url_save_list = []
    for u in data.find({'code',str(code)}):
        print(u)
        url_save_list.append(u['url'])#已经存过的url不爬取

    url_diff = [i for i in url_list if i not in url_save_list]
    for i,url in enumerate(url_diff):
        try:
            parse_datas = parse_news(url)
            parse_datas_list.append(parse_datas)
            # print(parse_datas)
        except:
            # print(html)
            parse_datas_list.append(url)
            # title_list.append(html)
    # print(date_list)
    print(len(parse_datas_list),parse_datas_list)
    print(len(url_list), url_list)
    print(len(title_list), title_list)
    print(len(date_list), date_list)
    return parse_datas_list, url_list, title_list, date_list

# code = '01538'
# url_list,date_list = parse(code)
# Crawl(code)
# parse_news('http://www.aastocks.com/sc/stocks/analysis/stock-aafn-content/01538/NOW.864362/hk-stock-news')

# import re
# a = 'NOW.821483'
# a.find(re.compile('N'))

