#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 多线程异步下载nyaso每日的图片 '

__author__ = 'fslong'

import asyncio
import json
import multiprocessing
import os
import random
import threading
import time
import traceback
import urllib
from io import BytesIO

import pyquery
import requests
import threading
from PIL import Image


class Nyaso(object):
    def __init__(self, *args, **kwargs):
        self.header = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.18204'
        }
        req = requests.get(
            'https://pic.nyaso.com/pixivday/', headers=self.header)
        s = str(req.cookies['check']).split('%2C')[1]
        # 使用urllib库中的unquote函数对s进行转换，url当中不能有特殊符号和中文所以，一般都进行了encode处理，如果想要进行encode处理的画可以使用：urllib.parse.quote(s)
        s = urllib.parse.unquote(s, encoding='utf-8')
        # print(s)
        self.urls = {
            'wallpaper': 'https://pic.nyaso.com/api/wallpaper.json',
            'pixiv': 'https://pic.nyaso.com/api/pixiv.json'
        }
        self.params = {
            'wallpaper': {
                't': 'new',
                'p': 1,
                's': s,
            },
            'pixiv': {
                't': 'daily',
                'p': 1,
                's': s,
            }
        }
        #self.cookies = {'Cookie': 'check=%s' % str(req.cookies['check'])}
        # print(self.cookies)

    async def getnysasoWallpaperPic(self, page, loop):
        params = self.params['wallpaper']
        params['p'] = page
        req = requests.get(
            self.urls['wallpaper'], params=params, headers=self.header)
        # print(req.text)
        dataJson = json.loads(req.text)

        def loop1(dataJson):
            for i in dataJson['lists']:
                self.getPic(os.path.join(os.path.dirname(__file__),'img'), i)

        t = threading.Thread(target=loop1, args=(dataJson, ))
        t.start()
        t.join()

    async def getnysasoPixivPic(self, page, loop):
        params = self.params['pixiv']
        params['p'] = page
        req = requests.get(
            self.urls['pixiv'], params=params, headers=self.header)
        # print(req.text)
        dataJson = json.loads(req.text)

        def loop1(dataJson):
            for i in dataJson['lists']:
                self.getPic(os.path.join(os.path.dirname(__file__),'img'), i)

        t = threading.Thread(target=loop1, args=(dataJson, ))
        t.start()
        t.join()

    def getPic(self, basePath, picDict):
        if 'wallPaper' in basePath:
            try:
                print(picDict['title'] + ':  ' + picDict['down'])
                req = requests.get(picDict['down'], headers=self.header)
                image = Image.open(BytesIO(req.content))
                image.save(
                    os.path.join(basePath, picDict['title']) + '.' +
                    picDict['down'].split('/')[-2])
            except:
                traceback.print_exc()

        else:
            try:
                print(picDict['title'] + ':  ' +
                      picDict['preview'].split('?')[0])
                req = requests.get(
                    picDict['preview'].split('?')[0], headers=self.header)
                # 将下载到的数据转换成bytesIo之后用image打开
                image = Image.open(BytesIO(req.content))
                image.save(os.path.join(basePath, picDict['title']) + '.jpg')
            except:
                traceback.print_exc()


if __name__ == '__main__':
    nyaso = Nyaso()
    loop = asyncio.get_event_loop()
    tasks = [nyaso.getnysasoPixivPic(i + 1, loop) for i in range(10)]
    loop.run_until_complete(asyncio.wait(tasks))
    #tasks = [nyaso.getnysasoWallpaperPic(i, loop) for i in [5]]
    # loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
