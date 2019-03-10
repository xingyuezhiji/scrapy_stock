#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/11 10:28
# @Author  : xingyuezhiji
# @Email   : zhong180@126.com
# @File    : login_tiantancha.py
# @Software: PyCharm Community Edition
#coding=utf-8
#!/usr/bin/env python
# encoding = utf-8

from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
from os import remove
import http.cookiejar as cookielib
from PIL import Image
import json
import re


class tiantancha(object):
    url = 'https://www.tianyancha.com/cd/login.json'

    # login_form_data = {'autoLogin':'true','cdpassword':"25990dae6bb33bcc8bc5ef0c3bd7cce1",'loginway':"PL",'mobile':"15622890079"}
    login_form_data ={"mobile": "15622890079", "cdpassword": "25990dae6bb33bcc8bc5ef0c3bd7cce1", "loginway": "PL"}
    headers = {'Host': 'www.tianyancha.com',
               'Referer': 'https://www.tianyancha.com/',

               'Content-Length': '105',
               'Connection': 'keep-alive',
               'Content-Type': 'application/json;charset=UTF-8',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Origin': 'https://www.tianyancha.com',
               'X-Requested-With': 'XMLHttpRequest',
               'Accept-Encoding': 'gzip, deflate, br'}
    headers1 = {}
    # headers1['Referer'] = 'https://www.tianyancha.com/usercenter/modifyInfo'
    # headers1['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    # headers1['Accept-Encoding']='gzip, deflate, sdch'

    session = None
    # print(headers)

    @classmethod
    def load_cookie(cls):
        """
        首先加载cookie
        :return:
        """
        cls.session = requests.session()
        cls.session.cookies = cookielib.LWPCookieJar(filename='Cookies_tyc')
        try:
            cls.session.cookies.load(ignore_discard=True)
        except BaseException as e:
            print(e)
            cls.login_form_data['mobile'] = input('请输入账号：')
            cls.login_form_data['cdpassword'] = input('请输入md5加密的密码：')
            cls.login_form_data['loginway'] = "PL"
            cls.login_form_data['autoLogin'] = True

    @classmethod

    def is_login(cls):
        """
        通过访问个人账户来判断是否已经登录
        :return:
        """
        url = "https://www.tianyancha.com/usercenter/modifyInfo"
        # print(url)
        login_code = cls.session.get(url, headers=cls.headers1,
                                     allow_redirects=False).status_code

        # print('111hhh')
        # print("is login")
        if login_code == 200:
            print("登录成功~")
            return True
        else:
            return False

    @classmethod

    def login(cls):
        cls.session = requests.session()
        cls.session.cookies = cookielib.LWPCookieJar(filename='Cookies_tyc')

        cls.session.post(cls.url, data=cls.login_form_data, headers=cls.headers)
        # 保存登录cookie
        cls.session.cookies.save()
        # 判断是否登录成功
        if not cls.is_login():
            print("登录失败，请重新尝试～")

    @classmethod
    def tyc_score(cls,keyword):
        headers = {'User-Agent': 'User-Agent:Mozilla/5.0'}
        # name = ''
        url = 'https://www.tianyancha.com/search?key={}'.format(keyword)
        response = requests.get(url, headers=headers)

        try:
            url_data = response.text.encode(response.encoding)
        except:
            url_data = response.text

        # print(html_data)
        soup = BeautifulSoup(url_data, 'lxml', from_encoding='utf-8')

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

    
    @classmethod
    def main(cls,keyword):
        url = "https://www.tianyancha.com/usercenter/modifyInfo"
        tiantancha.load_cookie()

        login_code = cls.session.get(url,
                                     allow_redirects=True).status_code
        requests.request(method='GET', url=url)
        # 判断是否登录
        if not tiantancha.is_login():
            tiantancha.login()
            score=0
        #     result_dict = tiantancha.search(keyword)
        else:
            score = tiantancha.tyc_score(keyword)

        print(score)
        return score


if __name__ == '__main__':
    tiantancha.main('孟筱茜')

