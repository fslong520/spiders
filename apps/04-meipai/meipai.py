#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 美拍 '

__author__ = 'fslong'

import asyncio
import base64
import os
import time
import traceback

import pyquery
import requests

from spider import Spider


class Meipai(Spider):
    def getTitlePic(self):
        '''# 美拍热门接口：
        self.url = 'http://www.meipai.com/home/hot_timeline'
        self.params = {'page': 1, 'count': 12}
        '''
        jsonData = self.downLoadJson(self.url, 'page' + str(1))
        print(jsonData)
    '''未弄明白美拍视频加密方式，尚未修复：
    def getVideo(self):
        self.url = 'http://www.meipai.com/media/1019039407'
        req = requests.get(self.url, headers=self.headers)
        PQreq = pyquery.PyQuery(req.text)
        urlBase64 = PQreq('.mp-h5-player-layer-video > video').attr('src')
        print(urlBase64)
    '''

    def getVideoTitlePicture(self, url):
        print('开始获取视频信息，请稍后...')
        self.url = url
        req = requests.get(self.url, headers=self.headers)
        PQreq = pyquery.PyQuery(req.text)
        picUrl = ''
        for i in PQreq('meta').items():
            if i.attr('property') == 'og:image':
                picUrl = i.attr('content')
        print('视频信息获取完毕，尝试下载封面图...')
        if picUrl != '':
            self.downLoadPic(picUrl, self.url.split('/')[-1])
        else:
            print('非常抱歉，封面图下载失败！')


if __name__ == '__main__':
    meipai = Meipai()
    meipai.getVideoTitlePicture(input('请输入要下载封面图的美拍视频地址：\n'))
