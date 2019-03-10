#encoding=utf-8
import sys
sys.path.append('G:\scrapy\ChineseNER/')
sys.path.append('/home/quant/zhong/scrapy/tmp/pycharm_project_221\ChineseNER/')

import requests
from collections import OrderedDict
import json
import re
import datetime
from pymongo import MongoClient
client = MongoClient('219.223.241.235', 27017)
# client = MongoClient('localhost', 27017)
db = client.stock
data = db.data
news = db.news
from login_qingbo import QingBo
from ChineseNER.main import evaluate_line1
import time
import numpy as np
import tushare as ts
from sklearn.linear_model import LinearRegression
import random




def prediction(j):
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
        stock_name = list(dict_json[i].values())[1]

        contents = []

        f1 = open('people\投资人1.txt', 'r')
        f2 = open('people\投资人1.txt', 'r')
        f3 = open('people\投资人1.txt', 'r')
        word = []
        for v in news.find({"name": stock_name}):
            tt = v['datetime']
            date = datetime.datetime.strptime(tt, '%Y/%m/%d %H:%M')
            t_delta = (datetime.datetime.now() - date).days
            # print(t_delta)

            if t_delta <= 30:  # 30天以内的新闻进行分析
                # print(''.join(v['content'].split()).replace(' ', ''))
                try:
                    position1 = v['content'].find('(')
                    position2 = v['content'].find(')')
                    position3 = v['content'].find(')', position2 + 1)

                    t_content = ''.join(
                        v['content'].replace(v['content'][position1:position3 + 1], '').split())[:-19]

                    contents.append(t_content.replace(' ', ''))
                except:
                    contents.append(''.join(v['content'].split()).replace(' ', ''))

                # 判断是否在词库中

                for line in f1.readlines():
                    line = line[:-1]
                    if ''.join(v['content'].split()).replace(' ', '').find(line) > -0.5:
                        word.append(line)
                for line in f2.readlines():
                    line = line[:-1]
                    if ''.join(v['content'].split()).replace(' ', '').find(line) > -0.5:
                        word.append(line)
                for line in f3.readlines():
                    line = line[:-1]
                    if ''.join(v['content'].split()).replace(' ', '').find(line) > -0.5:
                        word.append(line)

        if len(word) > 0:
            pre_score = 1
            print(stock_name + ' -- 新闻中含有词库中的实体:' + word[0] + ',预打分权重为1\n')
        else:
            pre_score = 0.9
            print(stock_name + ' -- 新闻中不含词库中的实体,预打分权重为0.9\n')

        if len(contents) == 0:
            print(stock_name + ' -- No recent news\n\n')

        elif len(contents) > 0:

            print(stock_name + ' has {} recent news:\n'.format(len(contents)))

            name_list = evaluate_line1(contents)
            name_list = [u for u in name_list if len(u) > 1]

            # self.text.update()
            if name_list == []:

                time.sleep(0.1)
            else:
                num_score_list = []
                mean_score_list = []
                for name in name_list:
                    # result_dict = {}
                    result_dict, result_dict_wx = QingBo.main(name)
                    print(name + '>>> 百度新闻提及量: ' + result_dict['百度新闻提及量']
                          + ', 百度提及量: ' + result_dict['百度提及量'] + ',微信文章数： ' + str(
                        result_dict_wx['data']) + '\n')

                    sum_score = np.sqrt(int(result_dict['百度新闻提及量'])) + np.sqrt(
                        int(result_dict['百度提及量'])) / 10 + 3 * np.sqrt(int(result_dict_wx['data']))
                    num_score = 100 * sum_score / (150 + sum_score)
                    num_score_list.append(num_score)
                    # mean_score_list.append(mean_score)

                total_score = (np.nanmean(num_score_list)) * pre_score
                # 寻找历史新闻打分
                u = data.find({'name': stock_name})
                u = u[0]
                code = u['code']
                print(code)

                flag = True
                rounds = 0
                # 获取连接备用
                while (flag and rounds <= 10):
                    try:
                        cons = ts.get_apis()
                        df = ts.bar(code=code, conn=cons, asset='X', start_date='2017-01-01', end_date='')
                        df1 = df[(df['close'] - df['open']) / df['open'] > 0.15]
                        print(df1)
                        ts.close_apis(cons)
                        flag = False
                    except:
                        rounds += 1

                if df1.empty:
                    print('Unable to find historical data increasing more than 15%')
                    pass
                else:
                    # history_news_list = []
                    v = news.find({'name': stock_name})
                    history_score_list = []
                    history_increase_list = []
                    for date1 in df1.index:
                        for vv in news.find({'name': stock_name}):
                            date2 = datetime.datetime.strptime(vv['datetime'], '%Y/%m/%d %H:%M')
                            delta_t = (date1 - date2).days
                            if delta_t >= 0 and delta_t <= 30:  # 超过阈值的时间的30天以内的新闻
                                # print(delta_t)
                                print(date1, date2)

                                try:
                                    position1 = vv['content'].find('(')
                                    position2 = vv['content'].find(')')
                                    position3 = vv['content'].find(')', position2 + 1)

                                    t_content = ''.join(
                                        vv['content'].replace(vv['content'][position1:position3 + 1],
                                                              '').split())[:-19]
                                    print(t_content)
                                except:
                                    t_content = ''.join(vv['content'].split()).replace(' ', '')

                                # history_news_list.append(vv['content'])
                                history_increase = ((df1.close - df1.open) / df1.open)[date1]
                                PER_list_history = evaluate_line1([t_content])
                                # print(self.text)
                                print(PER_list_history)
                                name_list = PER_list_history

                                name_list = [u for u in name_list if len(u) > 1]

                                if name_list == []:
                                    print('Entity list of the history news is empty')

                                else:
                                    num_score_list = []
                                    mean_score_list = []
                                    for name in name_list:
                                        # result_dict = {}
                                        result_dict, result_dict_wx = QingBo.main(name)

                                        print('compute ing...')
                                        time.sleep(0.1)


                                        sum_score = np.sqrt(int(result_dict['百度新闻提及量'])) + np.sqrt(
                                            int(result_dict['百度提及量'])) / 10 + 3 * np.sqrt(
                                            int(result_dict_wx['data']))
                                        num_score = 100 * sum_score / (150 + sum_score)
                                        num_score_list.append(num_score)
                                        # mean_score_list.append(mean_score)

                                    history_score = np.nanmean(num_score_list) * pre_score

                                    print('该股票涨幅大于15%时对应的历史新闻的' + '>>> 总分数为 >>>' + str(
                                        history_score) )

                                    history_increase_list.append(history_increase)
                                    if history_score in history_score_list:
                                        history_score_list.append(history_score + random.uniform(-0.005, 0.005))
                                    else:
                                        history_score_list.append(history_score)

                    if history_score_list != []:
                        print(history_score_list, history_increase_list)
                        x = np.array(list(history_score_list)).reshape(-1, 1)
                        y = np.array(list(history_increase_list)).reshape(-1, 1)
                        if len(set(history_score_list)) == 1 or len(set(history_increase_list)) == 1:
                            a = y[0] / x[0]
                            pre_increase = [[a[0] * total_score]]
                        else:
                            model = LinearRegression()
                            model.fit(x, y)
                            pre_increase = model.predict(total_score)
                        if pre_increase[0][0] * 100 > 20:
                            print('该新闻对应股票的预测涨幅为：' + str(
                                pre_increase[0][0] * 100) + '%' + '----建议：买入\n\n')

                            time_now = datetime.datetime.now()

                            count = 0
                            with open('predict.txt','r') as ff:
                                for text in ff.readlines():
                                    if stock_name + ' ' + str(time_now)[:10]  in text:
                                        count+=1
                            if count == 0:
                                with open('predict.txt','a') as f:
                                    f.write(stock_name + ' ' +str(time_now)[:19] + ' ' +'的预测涨幅为：' + str(
                                             pre_increase[0][0] * 100) + '%' + '----建议：买入\n')


                        else:
                            print('该新闻对应股票的预测涨幅为：' + str(
                                pre_increase[0][0] * 100) + '%' + '----建议：不买入\n\n')
                            time_now = datetime.datetime.now()

                            count = 0

                            with open('predict.txt', 'r') as ff:
                                for text in ff.readlines():
                                    if stock_name + ' ' + str(time_now)[:10] in text:
                                        count+=1

                            if count == 0:
                                with open('predict.txt', 'a') as f:
                                        f.write(stock_name + ' ' + str(time_now)[:19] +' ' +'的预测涨幅为：' + str(
                                        pre_increase[0][0] * 100) + '%' + '----建议：不买入\n')


                    else:
                        print('Increasing history stock news cannot find entity to score\n\n')


# time_now = datetime.datetime.now()
# print(str(time_now)[:19])
prediction(1)