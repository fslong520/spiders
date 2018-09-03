#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' acfun小姐姐跳舞 '

__author__ = 'fslong'

import asyncio, json
import base64
import os
import time
import traceback

import pyquery
import requests

from spider import Spider
from dict2MySql import MySQLConnection


class Acfun(Spider):
    def getDanceByPage(self, page=1):
        self.url = 'http://www.acfun.cn/list/getlist'
        self.params = {
            'channelId': 134,
            'sort': 0,
            'pageSize': 20,
            'pageNo': page
        }
        req = requests.get(self.url, params=self.params, headers=self.headers)
        try:
            danceJson = json.loads(req.text)
        except:
            traceback.print_exc()
            danceJson = {}
        finally:
            if danceJson != {}:
                for i in danceJson['data']['data']:
                    print('开始下载:%s的封面图' % i['title'])
                    self.downLoadPic(i['coverImage'],
                                     str(i['id']) + '-' + i['title'])
                    mySQl = MySQLConnection()
                    i['commentCount'] = str(i['id']) + '-' + str(
                        i['commentCount'])
                    mySQl.dictData = i
                    #mySQl.executeSQL()# 创建数据表，首次连接数据库需要。
                    mySQl.insertData(mySQl.dictData)
                self.results.append(danceJson['data']['data'])
                self.saveData2Json(self.results, 'acfun')

    def getDancer(self):
        pass

    def getDanceDetail(self):
        pass

    def getDancerDetail(self):
        pass


if __name__ == '__main__':
    acfun = Acfun()
    acfun.getDanceByPage()