#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 豆瓣爬虫 '

__author__ = 'fslong'


import ast  # 用于将字符串转为字典
import json
import multiprocessing
import os
import random
import re
import threading
import time
import traceback

import pyquery
import requests

from spiders.apps.spider import Spider


class Douban(Spider):
    def getBook250(self, items):
        self.url = 'https://book.douban.com/top250'
        for i in range(items):
            self.params = {'start': i*25}
            req = requests.get(self.url, params=self.params,
                               headers=self.headers)
            PQreq = pyquery.PyQuery(req.text)
            urls = []
            for i in PQreq('.pl2 > a').items():
                urls.append(i.attr.href)
            tObj = []
            for url in urls:
                t = threading.Thread(target=self.getBookDetail, args=(url,))
                t.start()
                tObj.append(t)
            for t in tObj:
                t.join()  # 为每个子线程添加join之后，主线程就会等这些子线程执行完之后再执行。

    def getBookDetail(self, url):
        req = requests.get(url, headers=self.headers)
        PQreq = pyquery.PyQuery(req.text)
        bookName = PQreq('#wrapper > h1').text()
        bookInfoStr = PQreq('#info').text()
        bookInfo = {}
        for i in bookInfoStr.split('\n'):
            try:
                bookInfo[i.split(':')[0]] = i.split(
                    ':')[1].replace(' ', '').replace('\xa0', '')
            except:
                bookInfo['i'] = i
        bookIntro = PQreq('.intro > p').text().replace(
            '\n', '').replace('\t', '').replace('\r', '')
        authorIntro = PQreq('.indent > div > .intro').text().replace(
            '\n', '').replace('\t', '').replace('\r', '')
        bookScore = PQreq('.rating_num').text()
        bookTag = []
        for i in PQreq('.tag').items():
            bookTag.append(i.text())
        self.num += 1
        self.results.append({
            'booId': self.num,
            'bookName': bookName,
            'bookScore': bookScore,
            'bookTag': bookTag,
            'bookInfo': bookInfo,
            'bookIntro': bookIntro,
            'authorIntro': authorIntro,
        })


if __name__ == '__main__':
    spider = Douban()
    spider.getBook250(10)
    bookInfo = spider.results[0]
    print(bookInfo)
    with open(os.path.join(os.path.dirname(spider.path), 'results/doubanBook250.json'), 'w', encoding='utf-8') as f:
        json.dump(spider.results, f, ensure_ascii=False)
