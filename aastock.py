#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 23:03
# @Author  : xingyuezhiji
# @Email   : zhong180@126.com
# @File    : aastock.py
# @Software: PyCharm Community Edition
#coding=utf-8
#encoding=utf-8

import requests
import json
import re
from bs4 import BeautifulSoup
from collections import OrderedDict
def aastock(i):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    # i = 2
    response = requests.get(url=
                            'http://www.aastocks.com/sc/resources/datafeed/gethkactivestock.ashx?mkt=1&catg=' + str(i),
                            headers=headers)
    # response.encoding = 'ISO-8859-1'
    json_response = response.content.decode()
    # print(response.encoding)
    # print(json_response,type(json_response))

    # json_response = re.search(r'')
    dict_json = json.loads(json_response)

    for i in range(len(dict_json)):
        dict_json[i] = OrderedDict(sorted(dict_json[i].items()), key=lambda t: t[0])
        a = dict_json[i]['chg']
        aa = re.search(r'<.+>(.+)<.+>', a)
        dict_json[i]['chg'] = aa.group(1)

        b = dict_json[i]['pctchg']
        bb = re.search(r'<.+>(.+)<.+>', b)
        dict_json[i]['pctchg'] = bb.group(1)
        # print(dict_json[i]['chg'])
    for i in range(len(dict_json)):
        a = []
        a.append(list(dict_json[i].values())[1])
        a.append(list(dict_json[i].values())[0])
        for val in list(dict_json[i].values())[2:-1]:
            a.append(val)
        print(a)

aastock(2)
# d = dict_json[1].values()
# d.split()

# import re
# test = "<span class='pos'>+0.080</span>"
#
# aa = re.search(r'<.+>(.+)<.+>', test)
# print(aa.group(1))