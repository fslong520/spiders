#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 一些政策网站的爬虫 '

__author__ = 'fslong'
__version__ = '0.0.1'


import json
import os,re

import pyquery
import requests


class Spider(object):
    def __init__(self):
        self.path = os.path.dirname(__file__)
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.18204',
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':
            'en-US,en,zh-CN;q=0.5',
            'Accept-Encoding':
            'gzip, deflate, br',
            'DNT':
            '1',
            'Connection':
            'keep-alive',
        }
        self.num = 0
        self.results = []
        self.params = {}
        self.cookies = {'Cookie': ''}
        self.newNewsNum=0
        with open(os.path.join(os.path.dirname(__file__),'新公告.txt'),'w+',encoding='utf-8') as f:
            f.write('欢迎使用！\n')


class Cqsaisi(Spider):

    # 获取经信委通知：
    def getJxw(self):
        print('\n开始查找经信委网站信息:\n----------------------')
        jsonData = []

        def getData(page):
            self.url = 'http://wjj.cq.gov.cn/MoreList/MoreList.asp'
            self.params = {'pageno': page, 'intSTID': 6791}
            req = requests.get(self.url, params=self.params,
                               headers=self.headers, timeout=15)
            PQ = pyquery.PyQuery(req.text)
            data = PQ('body > table > tr > td > table > tr > td > table').items()

            for i in data:
                if '共' in i('tr td').text():
                    pass
                else:
                    text = ''
                    for j in i('tr td').items():
                        text += j.text()
                    href = i('tr td a').attr('href').replace(u'\\', u'/')
                    jsonData.append({'标题': text, '网址': href})
        print('经信委网站近期通知公告数据获取中，请稍等...')
        for i in range(5):
            getData(i+1)
        print('经信委网站近期通知公告数据获取完毕，开始分析...')
        if os.path.isfile(os.path.join(os.path.dirname(__file__), 'jxw.json')):
            with open(os.path.join(os.path.dirname(__file__), 'jxw.json'), 'r', encoding='utf-8') as f:
                oldJsonData = json.load(f)
            m = 0
            newNews = []
            for i in jsonData:
                k = 0
                for j in oldJsonData:
                    if i['网址'] == j['网址']:
                        k += 1
                if k == 0:
                    m += 1
                    newNews.append({'标题': i['标题'], '网址': i['网址']})

            if m == 0:
                print('----------------------\n没有查找到新的通知公告！\n')
            else:
                print('----------------------\n找到了{0}条新纪录，如下：\n'.format(m))
                self.saveNewNews('-------------------------------\n经信委网站新公告:\n',newNews)
                for i in newNews:
                    print('标题：', i['标题'], '网址：', i['网址'])
        else:
            print('没有找到本地数据，开始显示所有获取到的信息...')
            self.saveNewNews('-------------------------------\n经信委网站新公告:\n',jsonData)
            for i in jsonData:
                print('标题：', i['标题'], '网址：', i['网址'])
        with open(os.path.join(os.path.dirname(__file__), 'jxw.json'), 'w+', encoding='utf-8') as f:
            json.dump(jsonData, f, ensure_ascii=False, indent=4)

    # 获取科技局通知：

    def getKjj(self):
        print('\n开始查找科技局网站信息:\n----------------------')
        jsonData = []

        def getData(clsId=230, PageIndex=2):
            self.url = 'http://www.cstc.gov.cn/Class.aspx'
            self.params = {'PageIndex': PageIndex, 'clsId': clsId}
            req = requests.get(self.url, params=self.params,
                               headers=self.headers, timeout=15)
            PQ = pyquery.PyQuery(req.text)
            cssChoose = '#ctl02 > table > tr > td > table > tr > td > span > table > tr > td > table >  tr > td > table >  tr'
            cssChoose2 = 'td:nth-child(2)'
            cssChoose3 = 'td:nth-child(3)'
            table = PQ(cssChoose).items()
            for i in table:
                if i(cssChoose2)('strong').text() == '':
                    if i(cssChoose2)('a').attr('href'):
                        jsonData.append(
                            {'标题': i(cssChoose2).text()+' '+i(cssChoose3).text(),
                             '网址': 'http://www.cstc.gov.cn'+str(i(cssChoose2)('a').attr('href'))
                             })
        print('科技局网站近期通知公告数据获取中，请稍等...')
        for i in range(5):
            getData(PageIndex=i+1)
        print('科技局网站近期通知公告数据获取完毕，开始分析...')

        if os.path.isfile(os.path.join(os.path.dirname(__file__), 'kjj.json')):
            with open(os.path.join(os.path.dirname(__file__), 'kjj.json'), 'r', encoding='utf-8') as f:
                oldJsonData = json.load(f)
            m = 0
            newNews = []
            for i in jsonData:
                k = 0
                for j in oldJsonData:
                    if i['网址'] == j['网址']:
                        k += 1
                if k == 0:
                    m += 1
                    newNews.append({'标题': i['标题'], '网址': i['网址']})

            if m == 0:
                print('----------------------\n没有查找到新的通知公告！\n')
            else:
                print('----------------------\n找到了{0}条新纪录，如下：\n'.format(m))
                self.saveNewNews('-------------------------------\n科技局网站新公告:\n',newNews)
                for i in newNews:
                    print('标题：', i['标题'], '网址：', i['网址'])
        else:
            print('没有找到本地数据，开始显示所有获取到的信息...')
            self.saveNewNews('-------------------------------\n科技局网站新公告:\n',jsonData)
            for i in jsonData:
                print('标题：', i['标题'], '网址：', i['网址'])

        with open(os.path.join(os.path.dirname(__file__), 'kjj.json'), 'w+', encoding='utf-8') as f:
            json.dump(jsonData, f, ensure_ascii=False, indent=4)





    # 获取商务委员会数据：
    def getSwwyh(self):
        print('\n开始查找商务委员会网站信息:\n----------------------')
        jsonData = []

        def getData(categoryId=137, pageIndex=0):
            self.url = 'http://wsy.cq.gov.cn/api/directive/contentList'
            self.data = {'showParamters': True, 'categoryId': categoryId,'pageIndex':pageIndex,'count':18}
            req = requests.post(self.url, data=self.data,
                               headers=self.headers, timeout=15)
            json1=json.loads(req.text,encoding='utf-8')
            for i in json1['page']['list']:
                jsonData.append({
                    '标题':i['title'].strip()+' '+re.match(r'(\D.*?)(\d*-\d*-\d*)(\.*)',i['url']).group(2),
                    '网址':'http://wsy.cq.gov.cn'+i['url']
                })
        print('商务委员会网站近期通知公告数据获取中，请稍等...')
        for i in range(4):
            getData(pageIndex=i+1)
        print('商务委员会网站近期通知公告数据获取完毕，开始分析...')

        if os.path.isfile(os.path.join(os.path.dirname(__file__), 'swwyh.json')):
            with open(os.path.join(os.path.dirname(__file__), 'swwyh.json'), 'r', encoding='utf-8') as f:
                oldJsonData = json.load(f)
            m = 0
            newNews = []
            for i in jsonData:
                if i in oldJsonData:   
                    pass
                else:                                
                    m += 1
                    newNews.append({'标题': i['标题'], '网址': i['网址']})

            if m == 0:
                print('----------------------\n没有查找到新的通知公告！\n')
            else:
                print('----------------------\n找到了{0}条新纪录，如下：\n'.format(m))
                self.saveNewNews('-------------------------------\n商务委员会网站新公告:\n',newNews)
                for i in newNews:
                    print('标题：', i['标题'], '网址：', i['网址'])
        else:
            print('没有找到本地数据，开始显示所有获取到的信息...')
            self.saveNewNews('-------------------------------\n商务委员会网站新公告:\n',jsonData)
            for i in jsonData:
                print('标题：', i['标题'], '网址：', i['网址'])

        with open(os.path.join(os.path.dirname(__file__), 'swwyh.json'), 'w+', encoding='utf-8') as f:
            json.dump(jsonData, f, ensure_ascii=False, indent=4)
        


# 获取发改委通知：

    def getFgw(self):
        print('\n开始查找发改委网站信息:\n----------------------')
        jsonData = []

        def getData(urlP=''):
            baseurl = 'http://www.cqdpc.gov.cn/xxgk/tzgg/index'
            self.url=baseurl+urlP+'.shtml'
            req = requests.get(self.url, headers=self.headers, timeout=15)
            PQ = pyquery.PyQuery(req.text)
            cssChoose = '.list > ul > li'            
            lists = PQ(cssChoose).items()
            for i in lists:
                jsonData.append({
                    '标题':i.text().strip(),
                    '网址':'http://www.cqdpc.gov.cn'+i('a').attr('href')
                })


        
        print('发改委网站近期通知公告数据获取中，请稍等...')
        for i in ['','_2','_3','_4','_5']:
            getData(i)
        
        print('发改委网站近期通知公告数据获取完毕，开始分析...')

        if os.path.isfile(os.path.join(os.path.dirname(__file__), 'fgw.json')):
            with open(os.path.join(os.path.dirname(__file__), 'fgw.json'), 'r', encoding='utf-8') as f:
                oldJsonData = json.load(f)
            m = 0
            newNews = []
            for i in jsonData:
                k = 0
                for j in oldJsonData:
                    if i['网址'] == j['网址']:
                        k += 1
                if k == 0:
                    m += 1
                    newNews.append({'标题': i['标题'], '网址': i['网址']})

            if m == 0:
                print('----------------------\n没有查找到新的通知公告！\n')
            else:
                print('----------------------\n找到了{0}条新纪录，如下：\n'.format(m))
                self.saveNewNews('-------------------------------\n发改委网站新公告:\n',newNews)
                for i in newNews:
                    print('标题：', i['标题'], '网址：', i['网址'])
        else:
            print('没有找到本地数据，开始显示所有获取到的信息...')
            self.saveNewNews('-------------------------------\n发改委网站新公告:\n',jsonData)
            for i in jsonData:
                print('标题：', i['标题'], '网址：', i['网址'])

        with open(os.path.join(os.path.dirname(__file__), 'fgw.json'), 'w+', encoding='utf-8') as f:
            json.dump(jsonData, f, ensure_ascii=False, indent=4)
    def saveNewNews(self,title,news):
        with open(os.path.join(os.path.dirname(__file__),'新公告.txt'),'a',encoding='utf-8') as f:
            f.write(title)
            for i in news:
                self.newNewsNum+=1
                f.write('序号：{0}  标题:{1}  网址:{2}\n'.format(self.newNewsNum,i['标题'],i['网址']))




if __name__ == '__main__':
    cqsaisi = Cqsaisi()
    try:
        cqsaisi.getJxw()
    except:
        print('经信委数据爬取出错，请联系作者处理。')
    try:
        cqsaisi.getKjj()
    except:
        print('科技局数据爬取出错，请联系作者处理。')
    try:
        cqsaisi.getSwwyh()
    except:
        print('商务委员会数据爬取出错，请联系作者处理。')
    try:
        cqsaisi.getFgw()
    except:
        print('发改委数据爬取出错，请联系作者处理。')
    print('\n-------------------------\n新通知公告获取完毕，谢谢使用，可以打开《新公告.txt》查看本次获取到的新通知。')
    input('-------------------------\n请按回车键退出...')
    
    
    
