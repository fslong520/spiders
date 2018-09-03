#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 猫眼top100 '

__author__ = 'fslong'


import asyncio
import base64
import json
import os
import random
import re
import time
import traceback

import pyquery
import requests


class Maoyan(object):
    def __init__(self):
        self.results = []
        self.baseUrl = 'https://maoyan.com/board/4'
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
        self.params = {}
        self.data = {}
        self.id = 0

    def getData(self,offset):
        self.params={'offset':offset}
        response = requests.get(
            self.baseUrl, params=self.params, headers=self.headers)
        pqPage = pyquery.PyQuery(response.text)
        dds = pqPage('.board-wrapper > dd').items()
        for i in dds:
            print(i)
            self.id += 1
            name = i('.movie-item-info > p > a').text()
            img = i('.board-img').attr('data-src').split('@')[0]
            star = i('.star').text()
            releasetime = i('.releasetime').text()
            url=i('.movie-item-info > p > a').attr('href')
            score = i('.score').text()
            self.results.append({
                'id':self.id,
                'name': '《%s》'%name,
                'url':'https://maoyan.com'+url,
                'img': img,
                'star': star,
                'releasetime': releasetime,
                'score': score
            })

    def dumpData(self):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '猫眼电影TOP100.json'),'w',encoding='utf-8') as f:
            json.dump(self.results, f,ensure_ascii=False,indent=2)


if __name__ == '__main__':
    maoyan = Maoyan()
    for i in range(10):
        maoyan.getData(i*10)    
    maoyan.dumpData()
