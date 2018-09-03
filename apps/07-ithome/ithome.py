#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' it之家 '

__author__ = 'fslong'

import asyncio
import base64
import os
import time
import traceback

import pyquery
import requests

from spider import Spider


class Ithome(Spider):
    def getTitlePic(self, url):
        print('\n开始获取网页信息....')
        req = requests.get(url, headers=self.headers)
        print('网页信息获取完毕，开始分析...')
        PQreq = pyquery.PyQuery(req.text)
        keyword = PQreq('.news > main > h1').text()
        print(keyword)
        print('网页信息分析完毕,尝试查询新闻信息...')
        url = 'https://m.ithome.com/search/'+str(keyword)+'.htm'
        req = requests.get(url, headers=self.headers)
        print('网页信息获取完毕，开始分析...')
        PQreq = pyquery.PyQuery(req.text)
        picUrl = PQreq('.plc-image > img').attr('data-original')
        # print(picUrl)
        print('网页信息分析完毕,尝试下载封面图片...')
        if picUrl:
            self.downLoadPic(picUrl, url.split(
                '/')[-1].split('.')[0], show=True)
            print('封面图片下载成功，谢谢使用！\n')
        else:
            print('抱歉，封面图片下载失败，谢谢合作！\n')


if __name__ == '__main__':
    ithome = Ithome()
    ithome.getTitlePic(input('请输入要下载封面图片的新闻地址：'))
