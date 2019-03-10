#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/2 16:21
# @Author  : xingyuezhiji
# @Email   : zhong180@126.com
# @File    : gui_new.py
# @Software: PyCharm Community Edition
#coding=utf-8

import time
import threading
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




        def loop():
            self.processButton()
            window.after(180000, loop)

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


        # self.text.pack(fill=X)
        self.text.pack(fill='both',expand='yes')

        self.text.insert(END,'Finding Result\n')

        self.text.see(END)
        loop()#循环执行
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


        for i in range(len(dict_json)): #排行榜前20
        # for i in range(5):#排行榜前五
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
            self.text.insert(END, (str(a)[1:-1]+',').ljust(59,"　") + " ")
            link = str(list(dict_json[i].values())[-2])
            self.text.insert(END, link + "\n\n", link)
            self.text.tag_config(link, foreground="blue", underline=True)

            self.text.tag_bind(link, "<Enter>", show_arrow_cursor)
            self.text.tag_bind(link, "<Leave>", show_xterm_cursor)
            self.text.tag_bind(link, "<Button-1>", handlerAdaptor(goto_aastock,str=link))

            # print(list(dict_json[i].values())[-2])

            save_dict = {}
            save_dict =OrderedDict(save_dict)
            info_list = crawl_info(list(dict_json[i].values())[-2])  # 爬取股票信息
            for l in range(0,len(info_list)):
                try:
                    if l <=0:
                        save_dict['_id'] = 'rank:'+str(i+1)+' '+list(dict_json[i].values())[1]+\
                                           datetime.datetime.now().strftime('%Y/%m/%d %H:%M')
                        save_dict['name'] = list(dict_json[i].values())[1]
                        save_dict['rank'] = i+1
                        save_dict['datetime'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M')
                        save_dict['code'] = list(dict_json[i].values())[-2]
                        print(list(dict_json[i].values())[1])
                        if j ==1:
                            save_dict['type'] = 'up'
                        elif j==2:
                            save_dict['type'] = 'down'
                    else:
                        # ret = re.search('\d+', info_list[l]).group()#正则匹配数字

                        a = info_list[l].find(':')  # 冒号出现的位置
                        save_dict[info_list[l][0:a]] = (info_list[l][a+1:]) #简历字典
                        # print(info_list[l][0:a - 1])
                        # print(info_list[l][a:])


                        self.text.insert(END, info_list[l] + " ")
                        time.sleep(0.1)
                        self.text.update()


                except Exception as e:
                    print(e)
                    continue

            print(save_dict)
            try:
                data.insert(save_dict) #插入到数据库
            except:
                print('Data has been saved!!!')

            self.text.insert(END, "\n\n\n")



            if is_do ==0:
                self.text.insert(END, "\n\n")
            elif is_do and i<=9:

                # parse_datas_list = []
                # html_list = []
                news_dict = OrderedDict()#新闻数据字典

                print(list(dict_json[i].values())[1])
                parse_datas_list, html_list, title_list,date_list= \
                    Crawl(list(dict_json[i].values())[-2])


                # info_list = crawl_info(list(dict_json[i].values())[-2])#爬取股票信息
                # print(title_list)
                n = min(len(html_list),len(title_list),len(date_list),len(parse_datas_list))
                url_list = []
                lista_dict = {}
                lista_1 = ["click0", "click1", "click2", "click3", "click4", "click5",
                           "click10", "click11", "click12", "click13", "click14", "click15",
                           ]
                lista_2 = ["click2_0", "click2_1", "click2_2", "click2_3", "click2_4", "click2_5",
                           "click2_10", "click2_11", "click2_12", "click2_13", "click2_14", "click2_15",
                           ]
                lista_3 = ["click3_0", "click3_1", "click3_2", "click3_3", "click3_4", "click3_5",
                           "click3_10", "click3_11", "click3_12", "click3_13", "click3_14", "click3_15",
                           ]
                lista_4 = ["click4_0", "click4_1", "click4_2", "click4_3", "click4_4", "click4_5",
                           "click4_10", "click4_11", "click4_12", "click4_13", "click4_14", "click4_15",
                           ]
                lista_5 = ["click5_0", "click5_1", "click5_2", "click5_3", "click5_4", "click5_5",
                           "click5_10", "click5_11", "click5_12", "click5_13", "click5_14", "click5_15",
                           ]

                lista_6 = ["click6_0", "click6_1", "click6_2", "click6_3", "click6_4", "click6_5",
                           "click6_10", "click6_11", "click6_12", "click6_13", "click6_14", "click6_15",
                           ]
                lista_7 = ["click7_0", "click7_1", "click7_2", "click7_3", "click7_4", "click7_5",
                           "click7_10", "click7_11", "click7_12", "click7_13", "click7_14", "click7_15",
                           ]
                lista_8 = ["click8_0", "click8_1", "click8_2", "click8_3", "click8_4", "click8_5",
                           "click8_10", "click8_11", "click8_12", "click8_13", "click8_14", "click8_15",
                           ]
                lista_9 = ["click9_0", "click9_1", "click9_2", "click9_3", "click9_4", "click9_5",
                           "click9_10", "click9_11", "click9_12", "click9_13", "click9_14", "click9_15",
                           ]
                lista_10 = ["click10_0", "click10_1", "click10_2", "click10_3", "click10_4", "click10_5",
                           "click10_10", "click10_11", "click10_12", "click10_13", "click10_14", "click10_15",
                           ]


                lista_dict['1'] = lista_1
                lista_dict['2'] = lista_2
                lista_dict['3'] = lista_3
                lista_dict['4'] = lista_4
                lista_dict['5'] = lista_5
                lista_dict['6'] = lista_6
                lista_dict['7'] = lista_7
                lista_dict['8'] = lista_8
                lista_dict['9'] = lista_9
                lista_dict['10'] = lista_10



                FUNC_TEMPLATE = "def {func}(event,list_): webbrowser.open(list_[{click}])"

                lista = lista_dict[str(i+1)][0:n]
                for k, fn in enumerate(lista): #前n-1条新闻

                    news_dict["_id"] = list(dict_json[i].values())[1]+html_list[k]
                    news_dict['name'] = list(dict_json[i].values())[1]
                    news_dict['title'] = title_list[k]
                    news_dict['datetime'] = date_list[k]
                    news_dict['content'] = parse_datas_list[k]
                    news_dict['url'] = html_list[k]
                    print(news_dict)
                    try:
                        news.insert(news_dict)
                    except:
                        print('News has been saved!')

                    # print(fn)
                    self.text.insert(END, title_list[k] + "\n")
                    self.text.insert(END, date_list[k] + "\n")
                    time.sleep(0.1)
                    self.text.update()
                    urls = html_list[k]
                    url_list.append(urls)
                    # print(url_list)

                    def show_arrow_cursor(event):
                        self.text.config(cursor='arrow')

                    def show_xterm_cursor(event):
                        self.text.config(cursor='xterm')

                    exec(FUNC_TEMPLATE.format(func=fn, click=k))
                    local_vars = dict(locals().items())

                    # def click(event,num):
                    #     print(url_list)
                    #
                    #     webbrowser.open(url_list[num])

                    def handlerAdaptor(fun, **kwds):
                        '''''事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧'''
                        return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

                    link = lista[k]
                    self.text.insert(END, urls + "\n\n\n", link)
                    self.text.tag_config(link, foreground="blue", underline=True)

                    self.text.tag_bind(link, "<Enter>", show_arrow_cursor)
                    self.text.tag_bind(link, "<Leave>", show_xterm_cursor)

                    self.text.tag_bind(link, "<Button-1>", handlerAdaptor(local_vars[link], list_=url_list))

            self.text.insert(END, "\n\n\n\n\n")

        print('Running...')
        self.text.insert(END, 'Running...\n')
        # self.text.insert(END, "\n\n\n\n")





WidgetsDemo()
