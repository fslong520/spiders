#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 爬虫 '

__author__ = 'fslong'

import ast  # 用于将字符串转为字典
import asyncio
import hashlib
import json
import multiprocessing
import os
import random
import re
import threading
import time
import traceback
# 用于存储照片的
from io import BytesIO

import pymysql
import pyquery
import requests
from PIL import Image


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
        self.cookies = {'Cookie': ''}

    # 如果相应文件夹不存在就创建：
    def createDir(self, dirName):

        # 如果指定目录不存在就创建：
        if not os.path.exists(
                os.path.join(os.path.dirname(__file__), dirName)):
            os.mkdir(os.path.join(os.path.dirname(__file__), dirName))

    # 下载指定网址图片的方法：
    def downLoadPic(self, url, picName=''):
        # 如果名称没有声明，那就使用时间戳来生成个名字：
        if picName == '':
            picName = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()
        self.createDir('img')
        try:
            req = requests.get(url, headers=self.headers)
            image = Image.open(BytesIO(req.content))
            image.show()
            # 如果网址中存了照片的文件信息，比如后缀名：
            if '.' in url:
                image.save(
                    os.path.join(
                        os.path.dirname(__file__),
                        'img/' + picName + '.' + url.split('.')[-1]))
            # 没有后缀名的话直接存成bmp就可以了，这是因为本身image这个变量的就是位图:
            else:
                image.save(
                    os.path.join(
                        os.path.dirname(__file__), 'img/' + picName + '.bmp'))
            print('图片保存完毕，请前往img目录下查看。')
            return None
        except:
            traceback.print_exc()

    # 下载保存html文件的方法：
    def downLoadHtml(self, url, htmlName=''):
        if htmlName == '':
            htmlName = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()
        self.createDir('html')
        try:
            req = requests.get(url, headers=self.headers)
            try:
                with open(
                        os.path.join(
                            os.path.dirname(__file__),
                            'html/' + htmlName + '.html'),
                        'w',
                        encoding='utf-8') as f:
                    f.write(req.content.decode('utf-8'))
            except:
                with open(
                        os.path.join(
                            os.path.dirname(__file__),
                            'html/' + htmlName + '.html'),
                        'w',
                        encoding='utf-8') as f:
                    f.write(req.text)
            print('html文件保存完毕，请前往html目录下查看。')
            return req
        except:
            traceback.print_exc()

    # 下载指定网址json的方法:
    def downLoadJson(self, url, jsonName=''):
        if jsonName == '':
            jsonName = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()
        self.createDir('json')
        try:
            req = requests.get(url, headers=self.headers)
            try:
                jsonData = json.loads(req.content.decode('utf-8'))
            except:
                jsonData = json.loads(req.text)
            finally:
                with open(
                        os.path.join(
                            os.path.dirname(__file__),
                            'json/' + jsonName + '.json'),
                        'w',
                        encoding='utf-8') as f:
                    json.dump(jsonData, f)
                print('json文件保存完毕，请前往json目录下查看。')
                return jsonData
        except:
            traceback.print_exc()

    # 存储dict到json的方法：
    def saveDict2Json(self, dictData, dictName=''):
        if dictName == '':
            dictName = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()
        self.createDir('json')
        try:
            with open(
                    os.path.join(
                        os.path.dirname(__file__),
                        'json/' + dictName + '.json'),
                    'w',
                    encoding='utf-8') as f:
                json.dump(dictData, f)
            print('json文件保存完毕，请前往json目录下查看。')
        except:
            traceback.print_exc()


if __name__ == "__main__":

    async def yiBu(i):
        print('第%s个异步进程' % i)
        print(threading.current_thread())

    def duoXianCheng(i):
        print('第%s个多线程' % i)
        print(threading.current_thread())

    start1 = time.time()
    for i in range(200):
        t = threading.Thread(target=duoXianCheng, args=(i, ))
        t.start()
        t.join()
    end1 = time.time()

    start2 = time.time()
    loop = asyncio.get_event_loop()
    tasks = [yiBu(i) for i in range(200)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    end2 = time.time()

    print('\n多线程时间%s' % (end1 - start1))
    print('\n异步线程时间%s' % (end2 - start2))
