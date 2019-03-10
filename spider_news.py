#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/1 22:09
# @Author  : xingyuezhiji
# @Email   : zhong180@126.com
# @File    : Spider_news.py
# @Software: PyCharm Community Edition
#coding=utf-8




import socket
from bs4 import BeautifulSoup as bs
# import pandas as pd

import requests

# 爬取新闻
def parse_news(title,url):
    title1 = title
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
    # print(soup)
    #新浪财经内容
    if 'sina.com.cn' in url:
        contexts = soup.find_all('p')
        try:
            title = soup.find(id='artibodyTitle').get_text()
        except:
            title = soup.find(class_='main-title').get_text()

        for i,context in enumerate(contexts):
            if i < len(contexts)-7:
                return title,context.get_text().strip('\n').replace("\n\n","\n")\
                    .replace("\n\n","\n").replace("\n\n","\n").replace("\n\n","\n")
    #东方财富网内容
    elif 'eastmoney.com' in url:
        contexts = soup.find_all('p')
        title = soup.find(class_='newsContent').find('h1').get_text()
        # print(title)
        for i, context in enumerate(contexts):
            if i < len(contexts):
                return (title,context.get_text().strip('\n').replace("\n\n\n", "\n")
                      .replace("\n\n", "\n").replace("\n\n", "\n")
                      .replace("\n\n", "\n").replace("\n\n", "\n"))
    #凤凰网内容
    elif 'ifeng.com' in url:
        contexts = soup.find(id='main_content').find_all('p')
        title = soup.find(id='artical').find('h1').get_text()
        # print(title)

        for i, context in enumerate(contexts):
            if title:
                return (title,context.get_text().strip('\n').replace("\n\n\n", "\n")
                      .replace("\n\n", "\n").replace("\n\n", "\n"))
            else:
                return (title1, context.get_text().strip('\n').replace("\n\n\n", "\n")
                        .replace("\n\n", "\n").replace("\n\n", "\n"))
    #金融界内容
    elif 'jrj.com.cn' in url:
        contexts = soup.find(class_='texttit_m1').find_all('p')

        title = soup.find(class_='titmain').find('h1').get_text()\
            .strip('\n').replace("\n\n","\n")
        # print(title)
        for i, context in enumerate(contexts):
            if title:
                return (title,context.get_text().strip('\n').replace("\n\n\n", "\n")
                      .replace("\n\n", "\n").replace("\n\n", "\n"))
            else:
                return (title1, context.get_text().strip('\n').replace("\n\n\n", "\n")
                        .replace("\n\n", "\n").replace("\n\n", "\n"))
    #同花顺
    elif 'stock.10jqka.com.cn' in url:
        contexts = soup.find(class_='main-text atc-content').find_all('p')
        title = soup.find(class_='main-fl fl').find('h2').get_text() \
            .strip('\n').replace("\n\n", "\n")


        for i, context in enumerate(contexts):
            if title:
                return (title,context.get_text().strip('\n').replace("\n\n\n", "\n")
                      .replace("\n\n", "\n").replace("\n\n", "\n"))
            else:
                return (title1, context.get_text().strip('\n').replace("\n\n\n", "\n")
                        .replace("\n\n", "\n").replace("\n\n", "\n"))


    #腾讯
    # elif 'stock.qq.com' in url or 'finance.qq.com' in url:
    elif 'qq.com' in url:

        contexts = soup.find(id='Cnt-Main-Article-QQ').find_all('p')


        title = soup.find(class_='hd').find('h1').get_text() \
            .strip('\n').replace("\n\n", "\n")

        # print(title)
        for i, context in enumerate(contexts):
            if title !='':
                return (title,context.get_text().strip('\n').replace("\n\n\n", "\n")
                      .replace("\n\n", "\n").replace("\n\n", "\n"))
            else:
                return (title1, context.get_text().strip('\n').replace("\n\n\n", "\n")
                        .replace("\n\n", "\n").replace("\n\n", "\n"))

    #搜狐
    elif 'sohu.com' in url:
        contexts = soup.find(class_='article').find_all('p')
        title = soup.find(class_='text-title').find('h1').get_text() \
            .strip('\n').replace("\n\n", "\n")

        for i, context in enumerate(contexts):
            if title:
                return (title,context.get_text().strip('\n').replace("\n\n\n", "\n")
                      .replace("\n\n", "\n").replace("\n\n", "\n"))
            else:
                return (title1, context.get_text().strip('\n').replace("\n\n\n", "\n")
                        .replace("\n\n", "\n").replace("\n\n", "\n"))

    #和讯
    elif 'hexun.com' in url:
        contexts = soup.find(class_='art_contextBox').find_all('p')
        title = soup.find(class_='layout mg articleName').find('h1').get_text() \
            .strip('\n').replace("\n\n", "\n")

        for i, context in enumerate(contexts):
            if title:
                return (title,context.get_text().strip('\n').replace("\n\n\n", "\n")
                      .replace("\n\n", "\n").replace("\n\n", "\n"))
            else:
                return (title1, context.get_text().strip('\n').replace("\n\n\n", "\n")
                        .replace("\n\n", "\n").replace("\n\n", "\n"))


    #网易
    elif 'money.163.com' in url:
        contexts = soup.find(class_='post_text').find_all('p')
        title = soup.find(class_='post_content_main').find('h1').get_text() \
            .strip('\n').replace("\n\n", "\n")

        for i, context in enumerate(contexts):
            if title:
                return (title,context.get_text().strip('\n').replace("\n\n\n", "\n")
                      .replace("\n\n", "\n").replace("\n\n", "\n"))
            else:
                return (title1, context.get_text().strip('\n').replace("\n\n\n", "\n")
                        .replace("\n\n", "\n").replace("\n\n", "\n"))

    #中金在线
    elif 'cnfol.com' in url:
        contexts = soup.find(class_='Article')
        title = soup.find(class_='artMain mBlock').find('h3').get_text() \
            .strip('\n').replace("\n\n", "\n")

        if title:
            return (title, contexts.get_text().strip('\n').replace("\n\n\n", "\n")
                    .replace("\n\n", "\n").replace("\n\n", "\n"))
        else:
            return (title1, contexts.get_text().strip('\n').replace("\n\n\n", "\n")
                    .replace("\n\n", "\n").replace("\n\n", "\n"))
    else:

        [script.extract() for script in soup.findAll('script')]
        [style.extract() for style in soup.findAll('style')]
        # reg1 = re.compile("<[^>]*>")
        # content = reg1.sub('', soup.prettify())
        if title:
            return title,soup.get_text().strip('\n').replace("\n\n","\n").replace("\n\n","\n").\
            replace("\n\n","\n").replace("\n\n","\n").replace("\n\n","\n")
        else:
            return title1,soup.get_text().strip('\n').replace("\n\n","\n").replace("\n\n","\n").\
            replace("\n\n","\n").replace("\n\n","\n").replace("\n\n","\n")




# 爬取新闻网址
def parse(name):
    socket.setdefaulttimeout(200)
    url = 'http://news.baidu.com/ns?word={}&tn=news&from=news' \
          '&cl=2&rn=20&ct=1&clk=sortbytime'.format(name)
    headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}

    # req = request.Request(quote(url,safe='/:?='), headers=headers)
    # response = request.urlopen(req)
    response = requests.get(url, headers=headers)
    # print(response.encoding)
    html_data = response.text.encode(response.encoding) #utf-8

    soup = bs(html_data, 'html.parser', from_encoding='utf-8')
    # print(soup)
    html_list = []
    date_list = []
    for i in range(1, 6):
        result = soup.find(id=str(i))
        # print(result)
        # link = result.find_element_by_class_name('c-title')
        links = result.find("a")['href']
        date = result.find(class_='c-author').get_text().replace("\n","").replace("\t\t","")
        date = str(date[-18:-1])
        html_list.append(links)
        date_list.append(date)
        # print(date_list)
        # print(links)
    return html_list,date_list



def Crawl(name):

    parse_datas_list = []
    # url = "https://baike.baidu.com/item/" + str(code)
    # get html page data
    # html_data = download(url)
    # print(len(html_data))
    # parse the html page data
    html_list,date_list = parse(name)
    title_list = []
    for html in html_list:
        try:
            title,parse_datas = parse_news(name,html)
            parse_datas_list.append(parse_datas)
            title_list.append(title)
            # print(parse_datas)
        except:
            print(html)
            parse_datas_list.append(html)
            title_list.append(html)
    # print(date_list)
    return parse_datas_list,html_list,title_list,date_list



# url = 'http://finance.sina.com.cn/stock/hkstock/ggscyd/2018-05-25/doc-ihaysviy7307243.shtml?source=cj&dv=1'
# parse_news(1,url)
# print(parse_datas)
# parse('三爱健康')
# a = Judge('北京')
# print(a)
# parse_news('1',url='http://stock.qq.com/a/20180531/013713.htm')
# print(content)

