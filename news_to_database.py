from spider_aastock_news import Crawl
from spider_stock import crawl_info
from pymongo import MongoClient
import datetime
# client = MongoClient('localhost',27017)
client = MongoClient('10.249.180.192', 27017)
db = client.stock
data = db.data
news = db.news
import requests
import json
from collections import OrderedDict
import re
import time


def aastock(j):

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    # i = 2
    response = requests.get(url=
                            'http://www.aastocks.com/sc/resources/datafeed/gethkactivestock.ashx?mkt=1&catg=' + str(
                                j),
                            headers=headers)
    # response.encoding = 'ISO-8859-1'
    json_response = response.content.decode()
    dict_json = json.loads(json_response)

    for i in range(len(dict_json)):
        dict_json[i] = OrderedDict(sorted(dict_json[i].items()), key=lambda t: t[0])
        a = dict_json[i]['chg']
        aa = re.search(r'<.+>(.+)<.+>', a)
        dict_json[i]['chg'] = aa.group(1)

        b = dict_json[i]['pctchg']
        bb = re.search(r'<.+>(.+)<.+>', b)
        dict_json[i]['pctchg'] = bb.group(1)

    for i in range(len(dict_json)):  # 排行榜前15

        a = []

        a.append(list(dict_json[i].values())[1])
        a.append(list(dict_json[i].values())[0])

        for val in list(dict_json[i].values())[2:-2]:
            a.append(val)

        save_dict = {}
        save_dict = OrderedDict(save_dict)
        info_list = crawl_info(list(dict_json[i].values())[-2])  # 爬取股票信息
        for l in range(0, len(info_list)):
            try:
                if l <= 0:
                    save_dict['_id'] = 'rank:' + str(i + 1) + ' ' + list(dict_json[i].values())[1] + \
                                       datetime.datetime.now().strftime('%Y/%m/%d %H:%M')
                    save_dict['name'] = list(dict_json[i].values())[1]
                    save_dict['rank'] = i + 1
                    save_dict['datetime'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M')
                    save_dict['code'] = list(dict_json[i].values())[-2]
                    print(list(dict_json[i].values())[-2])
                    print(list(dict_json[i].values())[1])
                    if j == 1:
                        save_dict['type'] = 'up'
                    elif j == 2:
                        save_dict['type'] = 'down'
                else:
                    # ret = re.search('\d+', info_list[l]).group()#正则匹配数字

                    a = info_list[l].find(':')  # 冒号出现的位置
                    save_dict[info_list[l][0:a]] = (info_list[l][a + 1:])  # 简历字典

            except Exception as e:
                print(e)
                continue

        print(save_dict)
        try:
            data.insert(save_dict)  # 插入到数据库
        except:
            print('Data has been saved!!!')

        if i <= 15:

            # parse_datas_list = []
            # html_list = []
            news_dict = OrderedDict()  # 新闻数据字典

            print(list(dict_json[i].values())[1])
            parse_datas_list, html_list, title_list, date_list = \
                Crawl(list(dict_json[i].values())[-2])

            # info_list = crawl_info(list(dict_json[i].values())[-2])#爬取股票信息
            # print(title_list)
            n = min(len(html_list), len(title_list), len(date_list), len(parse_datas_list))

            for k in range(n):  # 前n-1条新闻
                news_dict["_id"] = list(dict_json[i].values())[1] + html_list[k]
                news_dict['name'] = list(dict_json[i].values())[1]
                news_dict['title'] = title_list[k]
                news_dict['datetime'] = date_list[k]
                news_dict['content'] = parse_datas_list[k]
                news_dict['url'] = html_list[k]
                news_dict['code'] = list(dict_json[i].values())[-2]
                print(news_dict)
                try:
                    news.insert(news_dict)
                except:
                    print('News has been saved!')

# aastock(1)
# aastock(2)
def main(h1=9,h2=17, m=10,d=7):
    '''h表示设定的小时，m为设定的分钟'''
    while True:
        # 判断是否达到设定时间，例如0:00
        while True:
            now = datetime.datetime.now()
            # 到达设定时间，结束内循环
            #if now.hour>=h1 and now.hour<=h2 and now.minute%m==0 and now.weekday()%d !=5 and now.weekday()%d !=6:
            if 2>1:
                try:
                    aastock(1)
                except:
                    pass

                try:
                    aastock(2)
                except:
                    pass

            # 不到时间就等20秒之后再次检测
            time.sleep(20)
            print('doing...')



main()

