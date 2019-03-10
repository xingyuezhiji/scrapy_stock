import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import ChineseNER.rnncell as rnn
# from ChineseNER.model import Model
import sys
sys.path.append('G:\scrapy\ChineseNER/')
import re
from ChineseNER.main import evaluate_line1
import pymongo
from pymongo import MongoClient
import datetime
import time
client = MongoClient('localhost',27017)
db = client.stock
data = db.data
news = db.news

def extract_name(stock_name,rank,type):
    name_set = set()
    contents = []
    news_to_extract = {}
    news_to_extract['rank'] = rank
    news_to_extract['name'] = stock_name
    if type == 1:
        news_to_extract['type'] = 'up'
    elif type==2:
        news_to_extract['type'] = 'down'
    for u in data.find(news_to_extract):
        name_set.add(u['name'])

    for nn in name_set:
        for v in news.find({"name": nn}):
            tt = v['datetime']
            date = datetime.datetime.strptime(tt, '%Y/%m/%d %H:%M')
            t_delta = (datetime.datetime.now()-date).days
            print(t_delta)
            if t_delta <=365:    #三天以内的新闻进行分析
            # print(''.join(v['content'].split()).replace(' ', ''))
                contents.append(''.join(v['content'].split()).replace(' ', ''))
            else:
                print('No recent news')


    PER_list = evaluate_line1(contents)
    # print(list(PER_list))
    PER_list = [u for u in PER_list if len(u) > 1]
    print(PER_list)
    return PER_list

# tfidf = analyse.extract_tags
# 引入TextRank关键词抽取接口
# textrank = analyse.textrank




headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}

def tyc_score(name):
    proxy = {'http':'114.99.27.132:40939'}
    # driver = webdriver.Chrome('phantomjs-2.1.1-windows/bin\phantomjs')
    # driver = webdriver.Chrome('chromedriver_win32\chromedriver')
    #
    # driver.get('https://www.tianyancha.com/login')
    # time.sleep(1.6)
    # user = driver.find_element_by_xpath(
    #     '//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/input')
    #
    # user.send_keys('15622890079')
    # time.sleep(2.6)
    # password = driver.find_element_by_xpath(
    #     '//*[@id="web-content"]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/input')
    #
    # password.send_keys('987456zjb')
    # time.sleep(0.8)
    # password.send_keys(Keys.ENTER)
    # driver.get('https://www.tianyancha.com/search?key={}'.format(name))
    # # click = driver.find_element_by_id("home-main-search")
    # # click.send_keys(name)
    # # click.send_keys(Keys.ENTER)
    #
    # # print(html_data)
    # soup = bs(driver.page_source, 'lxml')

    # contents = soup.find_all(class_='in-block vertical-middle float-right search-right-center')
    #
    # score = []
    # for content in contents[0:5]:
    #     content = content.get_text()[:-1]
    #     # print(content)
    #     try:
    #         score.append(int(content))
    #     except:
    #         score.append(60)
    # return score



    headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}
    # name = ''
    url = 'https://www.tianyancha.com/search?key={}'.format(name)


    response = requests.get(url, headers=headers,proxies=proxy)

    try:
        url_data = response.text.encode(response.encoding)
    except:
        url_data = response.text

    # print(html_data)
    soup = bs(url_data, 'lxml', from_encoding='utf-8')

    contents = soup.find_all(class_='in-block vertical-middle float-right search-right-center')

    score = []
    for content in contents[0:5]:
        content = content.get_text()[:-1]
        # print(content)
        try:
            score.append(int(content))
        except:
            score.append(60)
    return score

def find_company(name):
    headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}
    url2 = 'http://www.xizhi.com/search?wd={}&type=holder'.format(name)
    response2 = requests.get(url2, headers=headers)
    try:
        url_data2 = response2.text.encode(response2.encoding)
    except:
        url_data2 = response2.text
    soup2 = bs(url_data2, 'lxml', from_encoding='utf-8')
    contents2 = soup2.find(class_='result-list').find_all('li')
    # print(soup2)
    company_name_list = []
    for content2 in contents2:
        company_name = ''.join(content2.find('h3').get_text().split())
        company_name_list.append(company_name)
        # print(company_name)
    print(company_name_list)
    return company_name_list
    # print('')


def company_level(people_name):
    headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}
    # driver = webdriver.Chrome('chromedriver_win32\chromedriver')

    driver = webdriver.PhantomJS('phantomjs-2.1.1-windows/bin\phantomjs')
    driver.get('https://www.qichacha.com')

    searchkey = driver.find_element_by_id('searchkey')
    searchkey.send_keys(people_name)
    searchkey.send_keys(Keys.ENTER)
    company = driver.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
    name_list = []
    for c in company:
        print(c.find_element_by_tag_name('a').text)
        name_list.append(c.find_element_by_tag_name('a').text)
    for name in name_list:
        driver.get('http://www.bgcheck.cn/Index.html')
        input_Search = driver.find_element_by_id('input_Search')
        input_Search.send_keys(name)
        input_Search.send_keys(Keys.ENTER)
    for i in range(1, len(name_list)):
        try:
            windows = driver.window_handles
            driver.switch_to_window(windows[i])
            results = driver.find_element_by_id('content1').find_elements_by_tag_name('ul')
            try:
                for result in results:
                    result = result.text
                    company_level = re.search(r'信用等级：(.+)级', result).group(1).replace('  ', '')
                    company_rank = re.search(r'信用排名：(.+)\(', result).group(1)
                    print(company_level,company_rank)
                    # print(result.find_element_by_tag_name('span').text)
            except:
                print('no imformation')

            driver.close()
        except:
            print('None')


# a = '杭州京杭区块链科技有限公司'
# # jieba.
# print(tfidf(a))
# c = '北京小米科技有限责任公司  [信用等级：BBB级  信用排名：7719(-9)位  信用状况：信誉及形象一般  所属行业：机械设备  所在地区：北京]\
# 企业新闻\
# 注册号/信用码：110108012660422  经营状态：开业  注册资本：5000万元  企业类型：有限责任公司  企业法人：雷军\
# 注册地址：北京市海淀区永捷北路2号二层  成立日期：2010-03-03'
#
# print(re.search(r'信用等级：(.+)级',c).group(1).replace('  ',''))
# print(re.search(r'信用排名：(.+)\(',c).group(1))

# find_company('雷军')
# company_level('雷军')
# company_list =extract_name(1,1)
# company_list = extract_name('碧桂园服务',4,1)
# print(company_list)
# score = tyc_score('雷军')
# print(score)
# import numpy as np
# print(np.mean(score))



