#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/11 10:28
# @Author  : xingyuezhiji
# @Email   : zhong180@126.com
# @File    : login_qingbo.py
# @Software: PyCharm Community Edition
#coding=utf-8
#!/usr/bin/env python
# encoding = utf-8


import requests
import http.cookiejar as cookielib
import json
import re


class QingBo(object):
    url = 'http://www.gsdata.cn/member/login'
    url1 = 'http://www.gsdata.cn/tool/ajaxwebpagecount'
    url2 = 'http://www.gsdata.cn/user/accountpreview'
    login_form_data = {'username': '15622890079', 'password': '987456','remember': '1'}
    search_form_data = {'keyword': '马云','range': '0,1', 'accurate':'0'}
    search_form_data_wx = {'keyword': '马云', 'date1': '0', 'date2': '0'}
    url_wx = 'http://www.gsdata.cn/tool/ajaxwxnum'

    headers = {'Host': 'www.gsdata.cn',
               'Referer': 'http://www.gsdata.cn/member/login',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Accept-Encoding': 'gzip, deflate'}

    headers1 = headers.copy()
    headers1['Cookie'] = 'acw_tc=AQAAACjPDG8L8QUATW9J32ip18u8+TEM; _csrf-frontend=e8984e72ae84dc81ac592102265449af469eea6618cf39edd1641bac4fa62245a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22cAFR19IVGgnZDprmj56ol3KAh3BnDVa9%22%3B%7D; bdshare_firstime=1528625461863; Hm_lvt_293b2731d4897253b117bb45d9bb7023=1528625446,1528625555; _gsdataCL=WyIxMzcxNTAiLCIxNTYyMjg5MDA3OSIsIjIwMTgwNjEwMjA1NTE2IiwiZWQ1YzU3OGViOGY0ZWU5MGU2MzZkMDk3NWRkNWUzMjUiLDExNTYzOV0%3D; PHPSESSID=s7t8lsa89cq3rq7nuuts238tq0; _identity-frontend=d41fbb47b9d0b3833bc055d8b2cfe542b707b21b2a9726c1f764c83b8f7ae32ba%3A2%3A%7Bi%3A0%3Bs%3A18%3A%22_identity-frontend%22%3Bi%3A1%3Bs%3A26%3A%22%5B%22137150%22%2C%22test+key%22%2C3600%5D%22%3B%7D; Hm_lpvt_293b2731d4897253b117bb45d9bb7023=1528639192'
    headers1['Origin'] = 'http://www.gsdata.cn'
    headers1['Connection'] = 'keep-alive'
    headers1['Referer'] = 'http://www.gsdata.cn/tool/webpage'
    headers1['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    headers1['Content-Length'] = '58'
    headers1['X-Requested-With']='XMLHttpRequest'
    headers1['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

    # print(headers)

    headers_wx = {'Host': 'www.gsdata.cn','Connection': 'keep-alive','Content-Length': '51',
                  'Accept': 'application/json, text/javascript, */*; q=0.01','Origin': 'http://www.gsdata.cn',
                  'X-Requested-With': 'XMLHttpRequest','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','Referer': 'http://www.gsdata.cn/tool/wxnum',
                  'Accept-Encoding': 'gzip, deflate','Accept-Language': 'zh-CN,zh;q=0.9',
                  'Cookie': 'bdshare_firstime=1528625461863; acw_tc=AQAAAD0Ci3wG5QEATW9J38kVIhJhESUi; _csrf-frontend=7af3f42044df18fef64ebf02927bd7338d764d58b96b8bd3f6f987c1f91c9ca0a%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22l9YtKK1xq_Z8OIJ9TsW5A2JZ6RUZENEm%22%3B%7D; Hm_lvt_293b2731d4897253b117bb45d9bb7023=1528625446,1528625555,1530087667; _gsdataCL=WyIxMzcxNTAiLCIxNTYyMjg5MDA3OSIsIjIwMTgwNjI3MTYyMzM2IiwiNGI3OWVlMWRlYWM1N2VmNzY3OTc0OTQ1ZTM4YzQ1Y2UiLDExNTYzOV0%3D; PHPSESSID=4d8kmk4qb9058fga1qj8pvjg35; Hm_lpvt_293b2731d4897253b117bb45d9bb7023=1530099302'
    }
    session = None

    @classmethod
    def load_cookie(cls):
        """
        首先加载cookie
        :return:
        """
        cls.session = requests.session()
        cls.session.cookies = cookielib.LWPCookieJar(filename='cookies')
        try:
            cls.session.cookies.load(ignore_discard=True)
        except BaseException as e:
            print(e)
            cls.login_form_data['username'] = input('请输入账号：')
            cls.login_form_data['password'] = input(u'请输入密码：')

    @classmethod

    def is_login(cls):
        """
        通过访问个人账户来判断是否已经登录
        :return:
        """
        url = "http://www.gsdata.cn/user/index"
        # print(url)
        login_code = cls.session.get(url, headers=cls.headers,
                                     allow_redirects=False).status_code
        # print("is login")
        if login_code == 200:
            print("登录成功~")
            return True
        else:
            return False

    @classmethod

    def login(cls):
        cls.session = requests.session()
        cls.session.cookies = cookielib.LWPCookieJar(filename='cookies')

        cls.session.post(cls.url, data=cls.login_form_data, headers=cls.headers)
        # 保存登录cookie
        cls.session.cookies.save()
        # 判断是否登录成功
        if not cls.is_login():
            print("登录失败，请重新尝试～")

    @classmethod
    def search(cls,keyword):

        # r = cls.session.get(cls.url2, data=cls.search_form_data, headers=cls.headers)
        # cls.search_form_data
        cls.search_form_data['keyword'] = keyword
        r = cls.session.post(cls.url1, data=cls.search_form_data, headers=cls.headers1)

        print(r.text)

        json_response = r.content.decode()

        dict_json = json.loads(json_response)
        # print(dict_json['error_msg'])
        try:
            result = dict_json['error_msg']
            result = re.findall(r'<span>([0-9]+)</span>', result)
            result_dict = {}
            result_dict['百度提及量'] = result[0]
            result_dict['百度新闻提及量'] = result[1]
        except:
            result_dict = {}
            result_dict['百度提及量'] = '0'
            result_dict['百度新闻提及量'] = '0'

        print(result_dict)
        # print(type(result_dict))
        return result_dict

    @classmethod
    def search_wx(cls,keyword):
        cls.search_form_data['keyword'] = keyword
        r = cls.session.post(cls.url_wx, data=cls.search_form_data_wx, headers=cls.headers_wx)

        # print(r.text)
        try:
            json_response = r.content.decode()

            dict_json = json.loads(json_response)

        except:
            dict_json = {"error":0,"data":0}

        return dict_json


    @classmethod
    def main(cls,keyword):
        QingBo.load_cookie()

        # login_code = cls.session.get(url,
        #                              allow_redirects=True).status_code
        # requests.request(method='GET', url=url)
        # 判断是否登录
        # if not QingBo.is_login():
        #     QingBo.login()
        #     result_dict = QingBo.search(keyword)
        # else:

        result_dict = QingBo.search(keyword)
        result_dict_wx = QingBo.search_wx(keyword)
        # print(result_dict)
        return result_dict,result_dict_wx


if __name__ == '__main__':
    QingBo.main('马云')

