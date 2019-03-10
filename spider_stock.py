#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/5/29 17:21
# @Author  : xingyuezhiji
# @Email   : zhong180@126.com
# @File    : Spader_baike1.py
# @Software: PyCharm Community Edition
#coding=utf-8


from urllib import request
import socket
from bs4 import BeautifulSoup as bs
# import pandas as pd
from urllib.parse import quote
import requests
import json
from collections import OrderedDict

# 下载器
def download1(url):
    socket.setdefaulttimeout(200)
    if url is None:
        return None

    headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}

    req = request.Request(url, headers=headers)
    response = request.urlopen(req)
    if response.getcode() != 200:
        return None
    try:
        html_data = response.read().decode('gbk', 'ignore')  # .decode('gbk')
        return html_data
    except request.URLError as e:
        print("What")
        if hasattr(e, 'code'):
            print(e.code())
        if hasattr(e, 'reason'):
            print(e.reason())
# 下载器
def download(url):
    socket.setdefaulttimeout(200)
    if url is None:
        return None

    headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}

    req = request.Request(quote(url,safe='/:?='), headers=headers)
    response = request.urlopen(req)
    if response.getcode() != 200:
        return None
    try:
        html_data = response.read().decode('utf-8', 'ignore')  # .decode('gbk')
        return html_data
    except request.URLError as e:
        print("What")
        if hasattr(e, 'code'):
            print(e.code())
        if hasattr(e, 'reason'):
            print(e.reason())





def parse(html_cont):
    if html_cont is None:
        return
    soup = bs(html_cont, 'html.parser', from_encoding="utf-8")
    try:
        # <div class="detail-body" style="padding: 20px 50px;">
        list_table = soup.find(class_='deta03 clearfix')
        list_table = list_table.get_text().strip().split('\n')
        while '' in list_table:
            list_table.remove('')
        return list_table
    except Exception as e:
        print(e)

def parse1(html_cont):
    if html_cont is None:
        return
    soup = bs(html_cont, 'html.parser', from_encoding="utf-8")
    try:
        # <div class="detail-body" style="padding: 20px 50px;">
        list_table = soup.find(class_='deta01 clearfix')
        list_table = list_table.get_text().strip()
        # while '' in list_table:
        #     list_table.remove('')
        return list_table
    except Exception as e:
        print(e)




def crawl_stock(code):

    url = "http://stock.finance.sina.com.cn/hkstock/quotes/{}.html".format(code)
    # get html page data

    html_data = download1(url)
    parse_datas = parse(html_data)
                # parse_datas_list = parse_datas_list.append(parse_datas)
    # html_data = download1('http://stockpage.10jqka.com.cn/HK1059/')
    # parse_datas1 = parse1(html_data)
    print(parse_datas)
    # print(parse_datas1)
    # print(url)
    # print('\n')


    return parse_datas




def crawl_info(code):
    headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}

    response = requests.get(url='http://stockpage.10jqka.com.cn/HK%04d/quote/quotation/'
                                %int(code),headers=headers)#补足4位
    json_response = response.content.decode()

    dict_json = json.loads(json_response)
    # print(dict_json['data']['HK'+str(int('01538'))])
    try:
        dict_json['data']['HK%04d' % int(code)]['现价'] = dict_json['data']['HK%04d' % int(code)].pop('10')
        dict_json['data']['HK%04d' % int(code)]['成交量'] = dict_json['data']['HK%04d' % int(code)].pop('13')
        dict_json['data']['HK%04d' % int(code)]['成交额'] = dict_json['data']['HK%04d' % int(code)].pop('19')
        dict_json['data']['HK%04d' % int(code)]['市盈率'] = dict_json['data']['HK%04d' % int(code)].pop('2034120')
        dict_json['data']['HK%04d' % int(code)]['市净率'] = dict_json['data']['HK%04d' % int(code)].pop('592920')
        dict_json['data']['HK%04d' % int(code)]['均价'] = dict_json['data']['HK%04d' % int(code)].pop('1378761')
        dict_json['data']['HK%04d' % int(code)]['换手'] = dict_json['data']['HK%04d' % int(code)].pop('1968584')
        dict_json['data']['HK%04d' % int(code)]['昨收'] = dict_json['data']['HK%04d' % int(code)].pop('6')
        dict_json['data']['HK%04d' % int(code)]['今开'] = dict_json['data']['HK%04d' % int(code)].pop('7')
        dict_json['data']['HK%04d' % int(code)]['最高'] = dict_json['data']['HK%04d' % int(code)].pop('8')
        dict_json['data']['HK%04d' % int(code)]['最低'] = dict_json['data']['HK%04d' % int(code)].pop('9')
        dict_json['data']['HK%04d' % int(code)]['振幅'] = dict_json['data']['HK%04d' % int(code)].pop('526792')
        dict_json['data']['HK%04d' % int(code)]['总市值'] = dict_json['data']['HK%04d' % int(code)].pop('3475914')
        dict_json['data']['HK%04d' % int(code)]['流通市值'] = dict_json['data']['HK%04d' % int(code)].pop('3541450')
        dict_json['data']['HK%04d' % int(code)]['升跌幅'] = dict_json['data']['HK%04d' % int(code)].pop('264648')
        dict_json['data']['HK%04d' % int(code)]['升跌%'] = dict_json['data']['HK%04d' % int(code)].pop('199112')

        dict_json['data']['HK%04d' % int(code)] = \
            OrderedDict(sorted(dict_json['data']['HK%04d' % int(code)].items()), key=lambda t: len(t[1]))

        info_list = []
        for i, key in enumerate(dict_json['data']['HK%04d' % int(code)].keys()):
            if i >= 6 and i < len(dict_json['data']['HK%04d' % int(code)]) - 1:
                info_list.append(key + ':' + str(dict_json['data']['HK%04d' % int(code)][key]))
        # print(info_list)
        return info_list
    except:
        return ['0']*17





# crawl_stock('01889')
# code = '01051'
# crawl_info('00985')
# n = 123
# s = '{}'.format(n,'')
# s= '1234%04ddd'%n
# print(s)