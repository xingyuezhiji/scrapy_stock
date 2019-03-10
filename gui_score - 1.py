#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/11 15:51
# @Author  : xingyuezhiji
# @Email   : zhong180@126.com
# @File    : gui_score.py
# @Software: PyCharm Community Edition
#coding=utf-8

import numpy as np
import time
from spider_stock import crawl_info
from spider_aastock_news import Crawl
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import re
import requests
from urllib import request
import json
import re
from bs4 import BeautifulSoup
from collections import OrderedDict
import webbrowser

import pymongo
from pymongo import MongoClient
import datetime
from login_qingbo import QingBo
from scoring import extract_name
from scoring import tyc_score


client = MongoClient('localhost',27017)
db = client.stock
data = db.data
news = db.news

class WidgetsDemo:
    def __init__(self):
        window = Tk()  # 创建一个窗口
        window.maxsize(1200, 800)
        window.minsize(300, 240)
        window.title("Finding Engine")  # 设置标题

        frame1 = Frame(window)  # 创建一个框架
        frame1.pack()  # 将框架frame1放置在window中

        self.v1 = IntVar()
        self.v2 = IntVar()
        # 创建一个复选框，如果选中则self.v1为1,否则为0,当点击cbtBold时，触发processCheckbutton函数
        # cbtBold = Checkbutton(frame1, text="Volume", variable=self.v1,
        #                       command=self.processRadiobutton)




        # def loop():
        #     self.processButton()
        #     window.after(180000, loop)

        cbtBold = Radiobutton(frame1, text="Volume", bg="grey",
                            variable=self.v2, value=3,
                            command=self.processRadiobutton)

        # 创建两个单选按钮，放置在frame1中，按钮文本是分别是Red和Yellow，背景色分别是红色和黄色，
        # 当rbRed按钮被选中时self.v2为1,当rbYellow按钮被选中时，self.v2为2，按钮被点击时触发processRadiobutto函数
        rbRed = Radiobutton(frame1, text="Up", bg="red",
                            variable=self.v2, value=1,
                            command=self.processRadiobutton)
        rbYellow = Radiobutton(frame1, text="Down", bg="lime",
                               variable=self.v2, value=2,
                               command=self.processRadiobutton)

        stopName = Radiobutton(frame1, text="stop", bg="blue",
                               variable=self.v2, value=4,
                               command=self.processRadiobutton)


        # grid布局
        cbtBold.grid(row=1, column=3)
        rbRed.grid(row=1, column=1)
        rbYellow.grid(row=1, column=2)
        stopName.grid(row=1, column=4)

        frame2 = Frame(window)  # 创建框架frame2
        frame2.pack()  # 将frame2放置在window中

        # label = Label(frame2, text="Enter the stock: ")  # 创建标签
        # self.name = StringVar()
        self.content = StringVar()
        # # 创建Entry，内容是与self.name关联
        # entryName = Entry(frame2, textvariable=self.name)
        # # 创建按钮，点击按钮时触发processButton函数
        btGetName = Button(frame2, text="Start Finding",
                           command=self.processButton)

        def handlerAdaptor(fun, **kwds):
            return lambda fun=fun, kwds=kwds: fun(**kwds)

        stopName1 = Button(frame2, text="Stop",
                           command=self.processButton)


        # 创建消息
        # message = Message(frame2, text="It is a Finding Engine")

        # grid布局
        # label.grid(row=1, column=1)
        # entryName.grid(row=1, column=2)

        btGetName.grid(row=1, column=2)
        stopName1.grid(row=1, column=3)
        # message.grid(row=1, column=4)

        # 创建格式化文本，并放置在window中
        # self.text = Text(window)
        self.text = scrolledtext.ScrolledText(window,wrap=WORD,)

        #树状列表
        self.tree = ttk.Treeview(window)
        self.tree.pack(fill='both',expand='yes')


        # self.text.pack(fill=X)
        self.text.pack(fill='both',expand='yes')

        self.text.insert(END,'Finding Result\n')

        self.text.see(END)
        # loop()#循环执行
        # 监测事件直到window被关闭
        window.mainloop()



    def processRadiobutton(self):

        print('crawl infomation ing...')

        # global timer
        # timer = threading.Timer(5.5, self.processRadiobutton)


        # tr = Mythread()
        # tr.setDaemon(True)

        if self.v2.get()==3:
            # timer.start()
            self.aastock(3)
            self.text.see(END)

        elif self.v2.get()==1:

            # timer.start()
            self.aastock(1)
            self.text.see(END)
        elif self.v2.get()==2:

            # timer.start()
            self.aastock(2)
            self.text.see(END)
        else:
            # timer.cancel()
            print('finish!')

    global timer

    def processButton(self):
        # self.run(self.name.get())

        print('crawl infomation ing...')


        # timer = threading.Timer(5.5, self.processButton(1))
        self.aastock(1, is_do=1)
        self.text.insert(END, 'Seaching completed\n\n')
        self.text.see(END)

        self.aastock(2, is_do=1)
        self.text.insert(END, 'Seaching completed\n\n')
        self.text.see(END)


        # timer = threading.Timer(5.5, self.processButton)
        # timer.start()

    def score(self,i,j):
        name_list = extract_name(i, j)
        if name_list == []:
            self.text.insert(END, 'Name list is empty')
        else:
            for name in name_list:
                result_dict = QingBo.search(name)
                self.text.insert(END, result_dict)


    def aastock(self,j,is_do=0):


        def show_arrow_cursor(event):
            self.text.config(cursor='arrow')

        def show_xterm_cursor(event):
            self.text.config(cursor='xterm')

        def goto_aastock(event,str):
            webbrowser.open('http://www.aastocks.com/sc/ltp/'
                            'rtquote.aspx?symbol='+str)

        def handlerAdaptor(fun, **kwds):
            return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)


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
            # print(dict_json[i]['chg'])


        for i in range(len(dict_json)): #排行榜前20
        # for i in range(5):#排行榜前五
            if is_do ==0:
                label = '[名称         升跌       现价          时间          升跌%         代码]'
                if j == 1:
                    # if i==0:
                    self.text.insert(END, '最大升幅股票' + "\n")
                    self.text.insert(END, label + "\n\n")
                    self.text.focus_force()
                elif j == 2:
                    # if i == 0:
                    self.text.insert(END, '最大降幅股票' + "\n")
                    self.text.insert(END, label + "\n\n")
                    self.text.focus_force()
                elif j == 3:
                    # if i == 0:
                    self.text.insert(END, '最大成交额股票' + "\n")
                    self.text.insert(END, label + "\n\n")
                    self.text.focus_force()

                a = []

                a.append(list(dict_json[i].values())[1])
                a.append(list(dict_json[i].values())[0])

                for val in list(dict_json[i].values())[2:-2]:
                    a.append(val)
                # self.text.insert(END, str(a) + "\n")
                self.text.insert(END, (str(a)[1:-1] + ',').ljust(59, "　") + " ")
                link = str(list(dict_json[i].values())[-2])
                self.text.insert(END, link + "\n\n", link)
                self.text.tag_config(link, foreground="blue", underline=True)

                self.text.tag_bind(link, "<Enter>", show_arrow_cursor)
                self.text.tag_bind(link, "<Leave>", show_xterm_cursor)
                self.text.tag_bind(link, "<Button-1>", handlerAdaptor(goto_aastock, str=link))

                # print(list(dict_json[i].values())[-2])

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
                            print(list(dict_json[i].values())[1])
                            if j == 1:
                                save_dict['type'] = 'up'
                            elif j == 2:
                                save_dict['type'] = 'down'
                        else:
                            # ret = re.search('\d+', info_list[l]).group()#正则匹配数字

                            a = info_list[l].find(':')  # 冒号出现的位置
                            save_dict[info_list[l][0:a]] = (info_list[l][a + 1:])  # 遍历字典

                            self.text.insert(END, info_list[l] + " ")


                    except Exception as e:
                        print(e)
                        continue

                self.text.insert(END, "\n\n\n")
                # self.text.insert(END, "\n\n")


            elif is_do:
                print(i,j)
                if i <=9:
                    stock_name = list(dict_json[i].values())[1]
                    name_list = extract_name(stock_name, rank=(i + 1), type=j)  # rank:i+1 ,up:j=1;down:j=2
                    if name_list == []:
                        self.text.insert(END, 'Name list is empty')
                        time.sleep(0.1)
                        self.text.update()
                    else:

                        num_score_list = []
                        mean_score_list = []
                        for name in name_list:
                            # result_dict = {}
                            result_dict = QingBo.main(name)

                            self.text.insert(END,'Scrapying...' '\n')
                            time.sleep(0.1)
                            self.text.update()

                            score_list = tyc_score(name)

                            self.text.insert(END, 'Scrapying...' '\n')
                            time.sleep(0.1)
                            self.text.update()

                            mean_score = np.mean(score_list)
                            print(name + '>>> 百度新闻提及量: ' + result_dict['百度新闻提及量']
                                  + ', 百度提及量: ' + result_dict['百度提及量'] + '\n')

                            self.text.insert(END, name + '>>> 百度新闻提及量: ' + result_dict['百度新闻提及量']
                                             + ', 百度提及量: ' + result_dict['百度提及量'] + '\n')


                            sum_score = np.sqrt(int(result_dict['百度新闻提及量'])) + np.sqrt(int(result_dict['百度提及量']))
                            num_score = 100*sum_score/(150+sum_score)
                            num_score_list.append(num_score)
                            mean_score_list.append(mean_score)
                            self.text.insert(END,'百度提及量分数为：'+str(num_score)+'\n')
                            self.text.insert(END, '天眼查平均分数为：' + str(mean_score) + '\n')
                            time.sleep(0.1)
                            self.text.update()


                        self.text.insert(END, stock_name + '>>> 总分数为 >>>' + str(np.mean(mean_score_list)*0.6+0.4*np.mean(num_score_list))+ '\n')
                        time.sleep(0.1)
                        self.text.update()









            self.text.insert(END, "\n\n\n\n\n")


        self.text.insert(END, 'Running...\n')






WidgetsDemo()
