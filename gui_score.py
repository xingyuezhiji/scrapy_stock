#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/6/11 15:51
# @Author  : xingyuezhiji
# @Email   : zhong180@126.com
# @File    : gui_score.py
# @Software: PyCharm Community Edition
#coding=utf-8

import queue
import random
import sys
# sys.path.append('G:\scrapy\ChineseNER/')
# sys.path.append('/home/quant/zhong/scrapy/tmp/pycharm_project_221\ChineseNER/')
import numpy as np
from sklearn.linear_model import LinearRegression
import time
from spider_stock import crawl_info
# from spider_aastock_news import Crawl
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

import requests
# from urllib import request
import json
import re
# from bs4 import BeautifulSoup
from collections import OrderedDict
import webbrowser
import tushare as ts

# import pymongo
from pymongo import MongoClient
import datetime
from login_qingbo import QingBo
from scoring import extract_name
# from scoring import tyc_score
from ChineseNER.main import evaluate_line1

client = MongoClient('10.249.180.192', 27017)
# client = MongoClient('115.201.44.171', 57017)
# client = MongoClient('localhost', 27017)
db = client.stock
data = db.data
news = db.news

class WidgetsDemo:
    def __init__(self):
        window = Tk()  # 创建一个窗口
        window.maxsize(1500, 1200)
        window.minsize(300, 240)
        window.geometry("1150x800")
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

        stopName = Button(frame1, text="find all", bg="pink",

                               command=self.precessBotton1)


        # grid布局
        cbtBold.grid(row=1, column=3)
        rbRed.grid(row=1, column=1)
        rbYellow.grid(row=1, column=2)
        stopName.grid(row=1, column=4)

        frame2 = Frame(window)  # 创建框架frame2
        frame2.pack()  # 将frame2放置在window中

        # label = Label(frame2, text="Enter the stock: ")  # 创建标签
        self.name = StringVar()
        self.content = StringVar()
        # # 创建Entry，内容是与self.name关联
        entryName = ttk.Entry(frame2, textvariable=self.name)
        # # 创建按钮，点击按钮时触发processButton函数


        def handlerAdaptor(fun, **kwds):
            return lambda fun=fun, kwds=kwds: fun(**kwds)

        findName = Button(frame2, text="Press to Find",bg="skyblue",
                           command=self.processButton,)


        # 创建消息
        # message = Message(frame2, text="It is a Finding Engine")

        # grid布局
        # label.grid(row=1, column=1)
        entryName.grid(row=0, column=0,columnspan=3)

        # btGetName.grid(row=1, column=2)
        findName.grid(row=0, column=3,columnspan=2,)
        # message.grid(row=1, column=4)


        frame3 = Frame(window,height=10)  # 创建框架frame2
        frame3.pack()
        #树状列表
        # columns = ('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23')
        columns = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18','19','20','21','22','23','24')
        self.tree = ttk.Treeview(frame3,height=15,show="headings",columns=columns)


        vbar = ttk.Scrollbar(frame3, orient=VERTICAL, command=self.tree.yview)

        self.tree.configure(yscrollcommand=vbar.set)


        frame4 = Frame(window)  # 创建框架frame2
        frame4.pack()

        self.treeview = ttk.Treeview(frame4,height=20)
        # self.treeview.place(width=1000)
        vbar1 = ttk.Scrollbar(frame4, orient=VERTICAL, command=self.treeview.yview)

        self.treeview.configure(yscrollcommand=vbar1.set)

        # btGetName = Button(frame2, text="Finding all",
        #                    command=self.processButton)


        self.tree.pack(fill='both', expand='yes')

        self.treeview.pack(fill='both',side='left',ipadx=220)
        vbar1.pack(side='left', fill=Y)
        # vbar1.grid(row=0, column=3, columnspan=1, rowspan=6, sticky=W+N, ipady=200)
        show = StringVar()

        # Entry.pack()
        # 创建格式化文本，并放置在window中
        # self.text = Text(window)
        self.text = scrolledtext.ScrolledText(frame4,wrap=WORD)
        text = self.text


        self.text.pack(fill='both',side='bottom',ipadx=250)
        self.text.pack(fill='both',expand='yes')
        Entry2 = ttk.Entry(frame4)
        Entry1 = ttk.Entry(frame4)
        self.text.see(END)
        Entry = ttk.Entry(frame3, textvariable=show, width="30")





        class section:
            def onPaste(self):
                try:
                    self.text1 = window.clipboard_get()
                except TclError:
                    pass
                show.set(str(self.text1))

            def onCopy(self):
                self.text1 = entryName.get()
                window.clipboard_append(self.text1)

            def onCut(self):
                self.onCopy()
                try:
                    entryName.delete('sel.first', 'sel.last')
                except TclError:
                    pass

        class section1:
            def onPaste(self):
                try:
                    self.text1 = window.clipboard_get()
                except TclError:
                    pass
                show.set(str(self.text1))

            def onCopy(self):

                self.text1 = entryName.get()
                window.clipboard_append(self.text1)

            def onCut(self):
                self.onCopy()
                try:
                    entryName.delete('sel.first', 'sel.last')
                except TclError:
                    pass

            def turnTo(self):
                self.text1 = Entry.get()
                print(self.text1)
                if self.text1 != '':
                    webbrowser.open(self.text1)

            def evaluate(self):
                self.text1 = Entry1.get()  #新闻内容
                self.text2 = Entry2.get()  #股票名字
                # print(Entry.get(),Entry1.get(),Entry2.get())



                if self.text1 != '':

                    contents = []

                    f1 = open('people\投资人1.txt', 'r')
                    f2 = open('people\投资人1.txt', 'r')
                    f3 = open('people\投资人1.txt', 'r')
                    word = []

                    for line in f1.readlines():
                        line = line[:-1]
                        if self.text1.find(line) > -0.5:
                                    word.append(line)
                    for line in f2.readlines():
                        line = line[:-1]
                        if self.text1.find(line) > -0.5:
                                    word.append(line)
                    for line in f3.readlines():
                        line = line[:-1]
                        if self.text1.find(line) > -0.5:
                                    word.append(line)

                    if len(word) > 0:
                        pre_score = 1
                        text.insert(END, '该新闻中含有词库中的实体:' + word[0] + ',预打分权重为1\n')
                        text.update()
                    else:
                        pre_score = 0.9
                        text.insert(END,'该新闻中不含词库中的实体,预打分权重为0.9\n')
                        text.update()

                    text.insert(END,'analyze ing...\n')
                    text.update()
                    PER_list = evaluate_line1([self.text1])
                    # print(self.text)
                    print(PER_list)

                    name_list = PER_list

                    text.update()
                    name_list = [u for u in name_list if len(u) > 1]

                    text.update()

                    if name_list == []:
                        text.insert(END, 'Entity list of the news is empty\n\n\n')
                        time.sleep(0.1)
                        text.update()
                    else:
                        num_score_list = []
                        mean_score_list = []
                        for name in name_list:
                            # result_dict = {}
                            result_dict, result_dict_wx = QingBo.main(name)

                            text.insert(END, 'compute ing...' '\n')
                            time.sleep(0.1)
                            text.update()

                            # score_list = tyc_score(name)

                            text.update()

                            # mean_score = np.nanmean(score_list)
                            print(name + '>>> 百度新闻提及量: ' + result_dict['百度新闻提及量']
                                  + ', 百度提及量: ' + result_dict['百度提及量'] + ',微信文章数： '+ str(result_dict_wx['data']) +  '\n')

                            text.insert(END, name + '>>> 百度新闻提及量: ' + result_dict['百度新闻提及量']
                                             + ', 百度提及量: ' + result_dict['百度提及量'] + ',微信文章数： '+ str(result_dict_wx['data']) +  '\n')

                            sum_score = np.sqrt(int(result_dict['百度新闻提及量'])) + np.sqrt(int(result_dict['百度提及量']))/10 + 3*np.sqrt(int(result_dict_wx['data']))
                            num_score = 100 * sum_score / (150 + sum_score)
                            num_score_list.append(num_score)
                            # mean_score_list.append(mean_score)
                            text.insert(END, '百度提及量分数为：' + str(num_score) + '\n')
                            # text.insert(END, '天眼查平均分数为：' + str(mean_score) + '\n')
                            time.sleep(0.1)
                            text.update()

                        total_score = (np.nanmean(mean_score_list) * 0.6 + 0.4 * np.nanmean(num_score_list)) * pre_score
                        if np.isnan(mean_score_list).sum() == len(mean_score_list):
                            total_score = (np.nanmean(num_score_list)) * pre_score

                        text.insert(END, '该新闻的' + '>>> 总分数为 >>>' + str(total_score) + '\n\n')
                        time.sleep(0.1)
                        text.update()


                        #寻找历史新闻打分
                        u = data.find({'name': self.text2})
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
                            text.insert(END, 'Unable to find historical data increasing more than 15%\n\n\n')
                            text.update()
                            text.see(END)
                        else:
                            # history_news_list = []
                            v = news.find({'name': self.text2})
                            history_score_list = []
                            history_increase_list = []
                            for date1 in df1.index:
                                for vv in news.find({'name': self.text2}):
                                    date2 = datetime.datetime.strptime(vv['datetime'], '%Y/%m/%d %H:%M')
                                    delta_t = (date1 - date2).days
                                    if delta_t >= 0 and delta_t <= 30:
                                        # print(delta_t)
                                        print(date1, date2)

                                        try:

                                            position1 = vv['content'].find('(')
                                            position2 = vv['content'].find(')')
                                            position3 = vv['content'].find(')', position2 + 1)

                                            t_content = ''.join(
                                                vv['content'].replace(vv['content'][position1:position3+1], '').split())[:-19]

                                            print(t_content)
                                        except:
                                            t_content = ''.join(
                                                vv['content'].split()).replace(' ','')[:-19]

                                        # history_news_list.append(vv['content'])
                                        history_increase = ((df1.close - df1.open) / df1.open)[date1]
                                        PER_list_history = evaluate_line1([t_content])
                                        # print(self.text)
                                        print(PER_list_history)
                                        name_list = PER_list_history

                                        text.update()
                                        name_list = [u for u in name_list if len(u) > 1]
                                        text.update()
                                        if name_list == []:
                                            text.insert(END, 'Entity list of the history news is empty\n\n')
                                            time.sleep(0.1)
                                            text.update()
                                        else:
                                            num_score_list = []
                                            mean_score_list = []
                                            for name in name_list:
                                                # result_dict = {}
                                                result_dict, result_dict_wx = QingBo.main(name)

                                                text.insert(END, 'compute ing...' '\n')
                                                time.sleep(0.1)
                                                text.update()

                                                # score_list = tyc_score(name)

                                                text.update()

                                                # mean_score = np.nanmean(score_list)

                                                sum_score = np.sqrt(int(result_dict['百度新闻提及量'])) + np.sqrt(
                                                    int(result_dict['百度提及量']))/10 + 3*np.sqrt(int(result_dict_wx['data']))
                                                num_score = 100 * sum_score / (150 + sum_score)
                                                num_score_list.append(num_score)
                                                # mean_score_list.append(mean_score)

                                                time.sleep(0.1)
                                                text.update()
                                            # history_score = (np.nanmean(mean_score_list) * 0.6 + 0.4 * np.nanmean(
                                            #     num_score_list)) * pre_score

                                            history_score = np.nanmean(num_score_list) * pre_score

                                            # if np.isnan(mean_score_list).sum() == len(mean_score_list):
                                            #     history_score = (np.nanmean(num_score_list)) * pre_score
                                            #     print('hahahah')
                                            print(history_score)

                                            text.insert(END, '该股票涨幅大于15%时对应的历史新闻的' + '>>> 总分数为 >>>' + str(history_score) + '\n\n')
                                            time.sleep(0.1)
                                            text.update()

                                            history_increase_list.append(history_increase)
                                            if history_score in history_score_list:
                                                history_score_list.append(history_score + random.uniform(-0.005, 0.005))
                                            else:
                                                history_score_list.append(history_score)


                            if history_score_list!=[]:
                                print(history_score_list,history_increase_list)
                                x = np.array(list(history_score_list)).reshape(-1, 1)
                                y = np.array(list(history_increase_list)).reshape(-1, 1)
                                if len(set(history_score_list))==1 or len(set(history_increase_list))==1:
                                    a = y[0]/x[0]
                                    pre_increase = [[a*total_score]]
                                else:
                                    model = LinearRegression()
                                    model.fit(x, y)
                                    pre_increase = model.predict(total_score)
                                if pre_increase[0][0] * 100 >20:
                                    text.insert(END,'该新闻对应股票的预测涨幅为：'+str(pre_increase[0][0] * 100)+'%' + '----建议：买入\n\n\n')
                                    text.see(END)
                                    text.update()
                                else:
                                    text.insert(END, '该新闻对应股票的预测涨幅为：' + str(pre_increase[0][0] * 100) + '%' + '----建议：不买入\n\n\n')
                                    text.see(END)
                                    text.update()

                            else:
                                print('Increasing history stock news cannot find entity to score\n\n')
                                text.insert(END,'Increasing history stock news cannot find entity to score\n\n')
                                text.see(END)
                                text.update()

        section1 = section1()
        menu = Menu(window, tearoff=0)
        menu.add_command(label="复制", command=section1.onCopy)
        menu.add_separator()
        menu.add_command(label="粘贴", command=section1.onPaste)
        menu.add_separator()
        menu.add_command(label="剪切", command=section1.onCut)



        menu2 = Menu(window, tearoff=0)

        menu2.add_command(label="转到", command=section1.turnTo)
        menu2.add_separator()
        menu2.add_command(label="打分", command=section1.evaluate)


        def popupmenu(event):

            menu.post(event.x_root, event.y_root)


        def popupmenu1(event):
            item_id = event.widget.focus()
            item = event.widget.item(item_id)
            values = item['values']
            menu.post(event.x_root, event.y_root)
            entryName.delete(0, END)
            entryName.insert(END,values[1])

        def popupmenu2(event):
            item_id = event.widget.focus()
            item = event.widget.item(item_id)
            values = item['values']
            menu2.post(event.x_root, event.y_root)
            try:
                Entry.delete(0, END)
                # pass
                Entry.insert(END,values[0])
            except:
                pass
            try:
                Entry1.delete(0, END)
                Entry1.insert(END,values[1])
            except:
                pass

            try:
                Entry2.delete(0, END)
                Entry2.insert(END,values[2])
            except:
                pass


            # webbrowser.open(values[0])


        self.tree.bind("<Button-3>", popupmenu1)
        entryName.bind("<Button-3>", popupmenu)
        self.treeview.bind("<Button-3>", popupmenu2)


        # loop()#循环执行
        # 监测事件直到window被关闭
        window.mainloop()





    def processRadiobutton(self):

        print('crawl infomation ing...')


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
        # elif self.v1.get()==4:
        #     self.aastock(1, is_do=1)
        #     self.text.insert(END, 'Seaching completed\n\n')
        #     self.text.see(END)
        #     print('finish!')

    def precessBotton1(self):
        st_name = self.name.get()
        # self.aastock(1,is_do=0)
        # self.treeview.update()
        self.aastock(1, is_do=1)
        self.text.insert(END, 'Seaching completed\n\n')
        self.text.see(END)
        print('finish!')

    def processButton(self):

        print('crawl infomation ing...')
        stock_name = self.name.get()

        contents = []

        f1 = open('people/ceo.txt', 'r')
        f2 = open('people/投资人1.txt', 'r')
        f3 = open('people/自然人.txt', 'r')
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

                    t_content = ''.join(v['content'].replace(v['content'][position1:position3+1], '').split())[:-19]

                    contents.append(t_content.replace(' ', ''))
                except:
                    t_content = ''.join(v['content'].split())[:-19]

                    contents.append(t_content.replace(' ', ''))

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
            self.text.insert(END, stock_name + ' -- 新闻中含有词库中的实体:' + word[0] + ',预打分权重为1\n')
            self.text.update()
        else:
            pre_score = 0.9
            self.text.insert(END, stock_name + ' -- 新闻中不含词库中的实体,预打分权重为0.9\n')
            self.text.update()

        if len(contents) == 0:
            self.text.insert(END, stock_name + ' -- No recent news\n\n\n')
            self.text.update()

        elif len(contents) > 0:
            self.text.insert(END, 'analyze ing...\n')
            self.text.update()
            self.text.insert(END,
                             stock_name + ' has {} recent news:\n'.format(len(contents)))
            self.text.update()

            for n, content in enumerate(contents):


                name_list = evaluate_line1([content])
                # print(list(PER_list))
                self.text.update()
                name_list = [u for u in name_list if len(u) > 1]

                self.text.update()
                if name_list == []:
                    self.text.insert(END,
                                     stock_name + ' -- Entity list of News{} is empty\n'.format(n + 1))
                    time.sleep(0.1)
                    self.text.update()

                else:

                    self.text.insert(END,
                                     stock_name + ' -- Entity list of News{}:\n'.format(n + 1))
                    time.sleep(0.1)
                    self.text.update()

                    num_score_list = []
                    mean_score_list = []
                    for name in name_list:
                        # result_dict = {}
                        result_dict, result_dict_wx = QingBo.main(name)

                        self.text.insert(END, 'compute ing...' '\n')
                        time.sleep(0.1)
                        self.text.update()

                        # score_list = tyc_score(name)

                        self.text.update()

                        # mean_score = np.nanmean(score_list)


                        print(name + '>>> 百度新闻提及量: ' + result_dict['百度新闻提及量']
                              + ', 百度提及量: ' + result_dict['百度提及量'] + ',微信文章数： '+ str(result_dict_wx['data']) +  '\n')

                        self.text.insert(END, name + '>>> 百度新闻提及量: ' + result_dict['百度新闻提及量']
                                         + ', 百度提及量: ' + result_dict['百度提及量'] + ',微信文章数： '+ str(result_dict_wx['data']) +  '\n')

                        sum_score = np.sqrt(int(result_dict['百度新闻提及量'])) + np.sqrt(
                            int(result_dict['百度提及量']))/10 + 3*np.sqrt(int(result_dict_wx['data']))
                        num_score = 100 * sum_score / (150 + sum_score)

                        num_score_list.append(num_score)
                        # mean_score_list.append(mean_score)

                        self.text.insert(END, '百度提及量分数为：' + str(num_score) + '\n')
                        # self.text.insert(END, '天眼查平均分数为：' + str(mean_score) + '\n')
                        time.sleep(0.1)
                        self.text.update()


                        # total_score = (np.nanmean(mean_score_list) * 0.6 + 0.4 * np.nanmean(num_score_list))*pre_score
                        # if np.isnan(mean_score_list).sum() == len(mean_score_list):
                        total_score = (np.nanmean(num_score_list)) * pre_score

                    self.text.insert(END, stock_name + '>>> 总分数为 >>>' + str(total_score) + '\n')
                    time.sleep(0.1)
                    self.text.update()


                    self.text.insert(END, 'Finding history news of Transaction stock\n\n')

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
                        self.text.insert(END, 'Unable to find historical data increasing more than 15%\n\n')
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
                                    print(vv['content'])
                                    # history_news_list.append(vv['content'])
                                    history_increase = ((df1.close - df1.open) / df1.open)[date1]
                                    PER_list_history = evaluate_line1([vv['content']])
                                    # print(self.text)
                                    print(PER_list_history)
                                    name_list = PER_list_history

                                    self.text.update()
                                    name_list = [u for u in name_list if len(u) > 1]
                                    self.text.update()
                                    if name_list == []:
                                        self.text.insert(END, 'Entity list of the history news is empty\n\n')
                                        time.sleep(0.1)
                                        self.text.update()
                                    else:
                                        num_score_list = []
                                        mean_score_list = []
                                        for name in name_list:
                                            # result_dict = {}
                                            result_dict, result_dict_wx = QingBo.main(name)

                                            self.text.insert(END, 'compute ing...' '\n')
                                            time.sleep(0.1)
                                            self.text.update()

                                            # score_list = tyc_score(name)

                                            self.text.update()

                                            # mean_score = np.nanmean(score_list)

                                            sum_score = np.sqrt(int(result_dict['百度新闻提及量'])) + np.sqrt(
                                                int(result_dict['百度提及量']))/10 + 3*np.sqrt(int(result_dict_wx['data']))
                                            num_score = 100 * sum_score / (150 + sum_score)
                                            num_score_list.append(num_score)
                                            # mean_score_list.append(mean_score)

                                            time.sleep(0.1)
                                            self.text.update()

                                        history_score = np.nanmean(num_score_list) * pre_score

                                        # history_score = (np.nanmean(mean_score_list) * 0.6 + 0.4 * np.nanmean(
                                        #     num_score_list)) * pre_score
                                        #
                                        #
                                        # if np.isnan(mean_score_list).sum() == len(mean_score_list):
                                        #     history_score_score = (np.nanmean(num_score_list)) * pre_score

                                        self.text.insert(END, '该股票涨幅大于15%时对应的历史新闻的' + '>>> 总分数为 >>>' + str(
                                            history_score) + '\n\n')
                                        time.sleep(0.1)
                                        self.text.update()

                                        history_increase_list.append(history_increase)
                                        if history_score in history_score_list:
                                            history_score_list.append(history_score+random.uniform(-0.005,0.005))
                                        else:
                                            history_score_list.append(history_score)

                        if history_score_list != []:
                            print(history_score_list, history_increase_list)
                            x = np.array(list(history_score_list)).reshape(-1, 1)
                            y = np.array(list(history_increase_list)).reshape(-1, 1)
                            if len(set(history_score_list)) == 1 or len(set(history_increase_list)) == 1:
                                a = y[0] / x[0]
                                pre_increase = [[a * total_score]]
                            else:
                                model = LinearRegression()
                                model.fit(x, y)
                                pre_increase = model.predict(total_score)
                            if pre_increase[0][0] * 100 > 20:
                                self.text.insert(END, '该新闻对应股票的预测涨幅为：' + str(
                                    pre_increase[0][0] * 100) + '%' + '----建议：买入\n\n\n')
                                self.text.see(END)
                                self.text.update()
                            else:
                                self.text.insert(END, '该新闻对应股票的预测涨幅为：' + str(
                                    pre_increase[0][0] * 100) + '%' + '----建议：不买入\n\n\n')
                                self.text.see(END)
                                self.text.update()


                        else:
                            print('Increasing history stock news cannot find entity to score\n\n')
                            self.text.insert(END, 'Increasing history stock news cannot find entity to score\n\n')
                            self.text.see(END)
                            self.text.update()

            self.text.insert(END, '\n\n\n')

            self.text.update()
        self.text.update()

    def score(self,i,j):
        name_list = extract_name(i, j)
        if name_list == []:
            self.text.insert(END, 'Name list is empty')
        else:
            for name in name_list:
                result_dict = QingBo.search(name)
                self.text.insert(END, result_dict)


    def aastock(self,j,is_do=0):


        def on_double_click(event):


            item_id = event.widget.focus()
            item = event.widget.item(item_id)
            values = item['values']
            stock_name = values[1]
            news_to_extract = {}
            # news_to_extract['rank'] = values[0]
            news_to_extract['name'] = values[1]
            levelview_1 = self.treeview.insert('',0,text=stock_name)
            for order,u in enumerate(news.find(news_to_extract)):

                try:
                    position1 = u['content'].find('(')
                    position2 = u['content'].find(')')
                    position3 = u['content'].find(')', position2 + 1)

                    content = ''.join(u['content'].replace(u['content'][position1:position3+1], '').split())[:-19]


                except:
                    content = ''.join(u['content'].split())[:-19]

                levelview_2 = self.treeview.insert(levelview_1, 'end', text=u['datetime'] + '\t' + u['title'],
                                                   values=(u['url'], content, u['name']))

                # print(u)

                #按照字节长度截取字符串
                byte_content = content.encode('gbk')
                content_list = []
                temp = 0
                interval = 90
                for l in range(0, len(byte_content), interval):
                    try:
                        content_list.append(byte_content[temp:l + interval].decode('gbk'))
                        temp = l + interval
                    except:
                        content_list.append(byte_content[temp:l + interval - 1].decode('gbk'))
                        temp = l + interval - 1
                # print(content)
                # content = '\n'.join(content)#每隔30个字符换行
                if content_list==[]:
                    levelview_3 = self.treeview.insert(levelview_2, 0, text='None',values=(u['url'],content,u['name']))
                else:
                    for cc in content_list[-1::-1]:#从后往前插入
                        levelview_3 = self.treeview.insert(levelview_2,0, text=cc,values=(u['url'],content,u['name']))

                    # self.treeview.insert(levelview_2, 0, text=u['datetime'],values=(u['url'],u['content'],u['name']))



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

        #删除树
        if is_do==0:
            for _ in map(self.tree.delete, self.tree.get_children("")):
                pass

        for i in range(len(dict_json)): #排行榜前15
        # for i in range(5):#排行榜前五

            self.tree.update()

            if is_do ==0:
                label = '[名称         升跌       现价          时间          升跌%         代码]'

                label1 = ['rank','最大升幅股票','升跌','现价','时间','升跌%','代码']
                label2 = ['rank', '最大降幅股票', '升跌', '现价', '时间', '升跌%', '代码']
                label3 = ['rank', '最大成交额股票', '升跌', '现价', '时间', '升跌%', '代码']
                save_dict = {}
                save_dict = OrderedDict(save_dict)
                info_list = crawl_info(list(dict_json[i].values())[-2])  # 爬取股票信息
                print(info_list,len(info_list))
                feat_list = [] #股票特征列表
                feat_value_list = []
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
                            feat_list.append(info_list[l][0:a])
                            feat_value_list.append(info_list[l][a + 1:])
                            # self.text.insert(END, info_list[l] + " ")


                    except Exception as e:
                        print(e)
                        continue

                for feat in feat_list:
                    label1.append(feat)
                    label2.append(feat)
                    label3.append(feat)

                if j == 1:
                    # if i==0:
                    # self.text.insert(END, '最大升幅股票' + "\n")
                    # self.text.insert(END, label + "\n\n")

                    for l in range(len(label1)):
                        if l ==1:
                            self.tree.column(str(l+1), width=90, anchor='center')
                            # self.tree.heading(str(l+1), text=label1[l])
                            self.tree.heading(str(l+1), text=label1[l],
                                              command=lambda _col=str(l+1): treeview_sort_column(self.tree, _col, False))
                        elif l ==len(label1)-2:
                            self.tree.column(str(l + 1), width=70, anchor='center')
                            # level_1 = self.tree.heading(str(l + 1), text=label1[l])
                            self.tree.heading(str(l + 1), text=label1[l],
                                              command=lambda _col=str(l + 1): treeview_sort_column(self.tree, _col,False))
                        else:
                            self.tree.column(str(l + 1), width=45, anchor='center')
                            # self.tree.heading(str(l + 1), text=label1[l])
                            self.tree.heading(str(l + 1), text=label1[l],
                                              command=lambda _col=str(l + 1): treeview_sort_column(self.tree, _col,False))


                elif j == 2:
                    for l in range(len(label2)):
                        if l ==1:
                            self.tree.column(str(l+1), width=90, anchor='center')
                            # self.tree.heading(str(l+1), text=label1[l])
                            self.tree.heading(str(l+1), text=label2[l],
                                              command=lambda _col=str(l+1): treeview_sort_column(self.tree, _col, False))
                        elif l ==len(label2)-2:
                            self.tree.column(str(l + 1), width=70, anchor='center')
                            # level_1 = self.tree.heading(str(l + 1), text=label1[l])
                            self.tree.heading(str(l + 1), text=label2[l],
                                              command=lambda _col=str(l + 1): treeview_sort_column(self.tree, _col,False))
                        else:
                            self.tree.column(str(l + 1), width=45, anchor='center')
                            # self.tree.heading(str(l + 1), text=label1[l])
                            self.tree.heading(str(l + 1), text=label2[l],
                                              command=lambda _col=str(l + 1): treeview_sort_column(self.tree, _col,False))


                elif j == 3:
                    for l in range(len(label3)):
                        if l == 1:
                            self.tree.column(str(l + 1), width=90, anchor='center')
                            # self.tree.heading(str(l+1), text=label1[l])
                            self.tree.heading(str(l + 1), text=label3[l],
                                              command=lambda _col=str(l + 1): treeview_sort_column(self.tree, _col,
                                                                                                   False))
                        elif l == len(label3) - 2:
                            self.tree.column(str(l + 1), width=70, anchor='center')
                            # level_1 = self.tree.heading(str(l + 1), text=label1[l])
                            self.tree.heading(str(l + 1), text=label3[l],
                                              command=lambda _col=str(l + 1): treeview_sort_column(self.tree, _col,
                                                                                                   False))
                        else:
                            self.tree.column(str(l + 1), width=45, anchor='center')
                            # self.tree.heading(str(l + 1), text=label1[l])
                            self.tree.heading(str(l + 1), text=label3[l],
                                              command=lambda _col=str(l + 1): treeview_sort_column(self.tree, _col,
                                                                                                   False))

                a = []
                a.append(str(i+1)) #rank
                a.append(list(dict_json[i].values())[1])
                a.append(list(dict_json[i].values())[0])

                for val in list(dict_json[i].values())[2:-1]:
                    a.append(val)
                # self.text.insert(END, str(a) + "\n")

                for val in feat_value_list:
                    a.append(val)


                level_2 = self.tree.insert('',END,values=a[:])

                self.tree.bind("<Double-Button-1>", on_double_click)


                # self.text.insert(END, "\n\n\n")
                # self.text.insert(END, "\n\n")


            elif is_do:
                print(i,j)
                if i <=14:
                    stock_name = list(dict_json[i].values())[1]
                    # name_list = extract_name(stock_name, rank=(i + 1), type=j)  # rank:i+1 ,up:j=1;down:j=2
                    self.text.update()

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

                                t_content = ''.join(v['content'].replace(v['content'][position1:position3+1], '').split())[:-19]

                                contents.append(t_content.replace(' ', ''))
                            except:
                                contents.append(''.join(v['content'].split()).replace(' ', ''))


                            #判断是否在词库中

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
                        self.text.insert(END, stock_name + ' -- 新闻中含有词库中的实体:' + word[0] + ',预打分权重为1\n')
                        self.text.update()
                    else:
                        pre_score = 0.9
                        self.text.insert(END, stock_name + ' -- Rank{} --'.format(i + 1) + ' 新闻中不含词库中的实体,预打分权重为0.9\n')
                        self.text.update()



                    if len(contents) == 0:
                        self.text.insert(END, stock_name + ' -- Rank{} --'.format(i + 1) +' No recent news\n\n\n')
                        self.text.update()

                    elif len(contents)>0:
                        self.text.insert(END, 'analyze ing...\n')
                        self.text.update()
                        self.text.insert(END, stock_name + ' -- Rank{} --'.format(i + 1) + 'has {} recent news:\n'.format(len(contents)))
                        self.text.update()
                        self.text.insert(END, 'analyze ing...\n')
                        self.text.update()

                        # for n,content in enumerate(contents):

                        name_list = evaluate_line1(contents)

                        # print(list(PER_list))
                        self.text.update()
                        name_list = [u for u in name_list if len(u) > 1]

                        self.text.update()
                        if name_list == []:
                            self.text.insert(END,
                                             stock_name + ' -- Rank{} --'.format(
                                                 i + 1) + ' Entity list of News is empty\n')
                            time.sleep(0.1)
                            self.text.update()

                        else:

                            self.text.insert(END,
                                             stock_name + ' -- Rank{} --'.format(
                                                 i + 1) + ' Entity list of News:\n')
                            time.sleep(0.1)
                            self.text.update()

                            num_score_list = []
                            mean_score_list = []
                            for name in name_list:
                                # result_dict = {}
                                result_dict, result_dict_wx = QingBo.main(name)

                                self.text.insert(END, 'compute ing...' '\n')
                                time.sleep(0.1)
                                self.text.update()

                                # score_list = tyc_score(name)

                                self.text.update()

                                # mean_score = np.nanmean(score_list)
                                print(name + '>>> 百度新闻提及量: ' + result_dict['百度新闻提及量']
                                      + ', 百度提及量: ' + result_dict['百度提及量'] + ',微信文章数： '+ str(result_dict_wx['data']) +  '\n')

                                self.text.insert(END, name + '>>> 百度新闻提及量: ' + result_dict['百度新闻提及量']
                                                 + ', 百度提及量: ' + result_dict['百度提及量'] + ',微信文章数： '+ str(result_dict_wx['data']) +  '\n')

                                sum_score = np.sqrt(int(result_dict['百度新闻提及量'])) + np.sqrt(
                                    int(result_dict['百度提及量']))/10 + 3*np.sqrt(int(result_dict_wx['data']))
                                num_score = 100 * sum_score / (150 + sum_score)
                                num_score_list.append(num_score)
                                # mean_score_list.append(mean_score)
                                self.text.insert(END, '百度提及量分数为：' + str(num_score) + '\n')
                                # self.text.insert(END, '天眼查平均分数为：' + str(mean_score) + '\n')
                                time.sleep(0.1)
                                self.text.update()


                            # total_score = (np.nanmean(mean_score_list) * 0.6 + 0.4 * np.nanmean(num_score_list)) * pre_score
                            # if np.isnan(mean_score_list).sum() == len(mean_score_list):
                            total_score = (np.nanmean(num_score_list)) * pre_score

                            self.text.insert(END, stock_name + '>>> 总分数为 >>>' + str(total_score) + '\n')
                            time.sleep(0.1)
                            self.text.update()


                            self.text.insert(END,'Finding history news of Transaction stock\n\n')

                            # 寻找历史新闻打分
                            u = data.find({'name': stock_name})
                            u = u[0]
                            code = u['code']
                            print(code)


                            flag = True
                            rounds = 0
                            # 获取连接备用
                            while(flag and rounds<=10):
                                try:
                                    cons = ts.get_apis()
                                    df = ts.bar(code=code, conn=cons, asset='X', start_date='2017-01-01', end_date='')
                                    df1 = df[(df['close'] - df['open']) / df['open'] > 0.15]
                                    print(df1)
                                    ts.close_apis(cons)
                                    flag = False
                                except:
                                    rounds+=1


                            if df1.empty:
                                print('Unable to find historical data increasing more than 15%')
                                self.text.insert(END,'Unable to find historical data increasing more than 15%\n\n')
                                self.text.see(END)
                            else:
                                # history_news_list = []
                                v = news.find({'name': stock_name})
                                history_score_list = []
                                history_increase_list = []
                                for date1 in df1.index:
                                    for vv in news.find({'name': stock_name}):
                                        date2 = datetime.datetime.strptime(vv['datetime'], '%Y/%m/%d %H:%M')
                                        delta_t = (date1 - date2).days
                                        if delta_t >= 0 and delta_t <= 30:#超过阈值的时间的30天以内的新闻
                                            # print(delta_t)
                                            print(date1, date2)

                                            try:
                                                position1 = vv['content'].find('(')
                                                position2 = vv['content'].find(')')
                                                position3 = vv['content'].find(')', position2 + 1)

                                                t_content = ''.join(
                                                    vv['content'].replace(vv['content'][position1:position3+1], '').split())[:-19]
                                                print(t_content)
                                            except:
                                                t_content = ''.join(vv['content'].split()).replace(' ','')


                                            # history_news_list.append(vv['content'])
                                            history_increase = ((df1.close - df1.open) / df1.open)[date1]
                                            PER_list_history = evaluate_line1([t_content])
                                            # print(self.text)
                                            print(PER_list_history)
                                            name_list = PER_list_history

                                            self.text.update()
                                            name_list = [u for u in name_list if len(u) > 1]
                                            self.text.update()
                                            if name_list == []:
                                                self.text.insert(END, 'Entity list of the history news is empty\n\n')
                                                self.text.see(END)
                                                time.sleep(0.1)
                                                self.text.update()
                                            else:
                                                num_score_list = []
                                                mean_score_list = []
                                                for name in name_list:
                                                    # result_dict = {}
                                                    result_dict, result_dict_wx = QingBo.main(name)

                                                    self.text.insert(END, 'compute ing...' '\n')
                                                    time.sleep(0.1)
                                                    self.text.update()

                                                    # score_list = tyc_score(name)

                                                    self.text.update()

                                                    # mean_score = np.nanmean(score_list)

                                                    sum_score = np.sqrt(int(result_dict['百度新闻提及量'])) + np.sqrt(
                                                        int(result_dict['百度提及量']))/10 + 3*np.sqrt(int(result_dict_wx['data']))
                                                    num_score = 100 * sum_score / (150 + sum_score)
                                                    num_score_list.append(num_score)
                                                    # mean_score_list.append(mean_score)

                                                    time.sleep(0.1)
                                                    self.text.update()
                                                # if np.nanmean(mean_score_list) == 'nan':
                                                #     history_score_part1 = 70
                                                # else:
                                                #     history_score_part1 = np.nanmean(num_score_list)

                                                history_score = np.nanmean(num_score_list) * pre_score

                                                # history_score = (history_score_part1 * 0.6 + 0.4 * np.nanmean(
                                                #     num_score_list)) * pre_score
                                                # 
                                                #
                                                # if np.isnan(mean_score_list).sum() == len(mean_score_list):
                                                #     history_score = (np.nanmean(num_score_list)) * pre_score
                                                self.text.insert(END, '该股票涨幅大于15%时对应的历史新闻的' + '>>> 总分数为 >>>' + str(
                                                    history_score) + '\n\n')
                                                self.text.see(END)
                                                time.sleep(0.1)
                                                self.text.update()

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
                                        pre_increase = [[a * total_score]]
                                    else:
                                        model = LinearRegression()
                                        model.fit(x, y)
                                        pre_increase = model.predict(total_score)
                                    if pre_increase[0][0] * 100 > 20:
                                        self.text.insert(END, '该新闻对应股票的预测涨幅为：' + str(
                                            pre_increase[0][0] * 100) + '%' + '----建议：买入\n\n\n')
                                        self.text.see(END)
                                        self.text.update()
                                    else:
                                        self.text.insert(END, '该新闻对应股票的预测涨幅为：' + str(
                                            pre_increase[0][0] * 100) + '%' + '----建议：不买入\n\n\n')
                                        self.text.see(END)
                                        self.text.update()


                                else:
                                    print('Increasing history stock news cannot find entity to score\n\n')
                                    self.text.insert(END,
                                                     'Increasing history stock news cannot find entity to score\n\n')
                                    self.text.see(END)
                                    self.text.update()




                        self.text.insert(END,'\n\n\n')

                        self.text.update()
                    self.text.update()



        def treeview_sort_column(tv, col, reverse):  # Treeview、列名、排列方式
            try:
                l = [(float(tv.set(k, col).replace('+','').replace('%','')), k) for k in tv.get_children('')]
            except:
                l = [(tv.set(k, col), k) for k in tv.get_children('')]
            print(tv.get_children(''))
            l = sorted(l,reverse=reverse)  # 排序方式

            print(l)
            # rearrange items in sorted positions
            for index, (val, k) in enumerate(l):  # 根据排序后索引移动
                tv.move(k, '', index)
                print(k)
            tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题



WidgetsDemo()
