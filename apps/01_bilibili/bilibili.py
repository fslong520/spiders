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
import sys
import threading, asyncio
import time
import traceback

import pyquery
import requests

from spider import Spider
# 用于存储照片的
from io import BytesIO
from PIL import Image


class Bilibili(Spider):

    # 下载哔哩哔哩视频封面的函数:
    async def getTitlePic(self, url):
        self.url = url
        req = requests.get(self.url, headers=self.headers)
        PQreq = pyquery.PyQuery(req.text)
        for i in PQreq('meta').items():
            if i.attr.itemprop == 'image':
                print('封面图片地址是：%s' % i.attr.content)
                self.downLoadPic(i.attr.content, url.split('/')[-1])
                return i.attr.content

                
    # 下载用户信息的函数:



if __name__ == '__main__':

    # 一些处理网址的函数:
    def getTitlePic():
        bilibili = Bilibili()
        a = input('请输入要下载封面的视频代号,多个视频号请用,隔开。比如：av28334721,av28354064：')
        a = a.split(',')
        loop = asyncio.get_event_loop()
        tasks = [
            bilibili.getTitlePic('https://www.bilibili.com/video/' + i)
            for i in a
        ]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        for i in a:
            bilibili.downLoadHtml('https://www.bilibili.com/video/' + i)
