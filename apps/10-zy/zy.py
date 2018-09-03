#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 中药大全 '

__author__ = 'fslong'

import asyncio
import base64
import json
import os
import re
import time
import traceback, random

import pyquery
import requests, threading

from dict2MySql import MySQLConnection
from spider import Spider


class ZhongYao(Spider):
    async def getZhongYaoData(self, i):
        zhongyaoDB = MySQLConnection()
        zhongyaoDB.dbName = 'zhongyao'
        zhongyaoDB.tabName = 'zhongyao'
        results = zhongyaoDB.selectData('id', i)
        #results = ()
        if results == '()' or results == () or results == None:
            url = 'https://www.daquan.com/cyzy/zy%s.html' % str(i)
            zyid = i
            req = requests.get(url, headers=self.headers, timeout=15)
            PQreq = pyquery.PyQuery(req.content.decode('utf-8'))
            name = PQreq('.article > h1').text()
            detail = PQreq('.content > p')
            content = detail.text()
            content0 = content
            if not content0.split('【')[0] == '':
                name = content0.split('【')[0]
            if name == None or name == '':
                return None
            else:                
                content = self.creatFileName(content)
                contentList = content.split('【')
                if not content.split('【')[0] == '':
                    name = content.split('【')[0]
                if len(name) > 20:
                    name = name[0:20]
                contentDict = {'名称': name}
                for i in contentList:
                    if len(i.split('】')) > 1:
                        contentDict[i.split('】')[0]] = i.split('】')[1]
                pics = []
                for i in detail('img').items():
                    if not i.attr.src.startswith('http'):
                        pics.append('https://www.daquan.com' + i.attr.src)
                    else:
                        pics.append(i.attr.src)
                zhongyaoDict = ({
                    'id': zyid,
                    'name': name,
                    'content': contentDict,
                    'pics': pics
                })
                #self.results.append(zhongyaoDict)
                #self.saveData2Json(self.results, 'zhongyao')
                # 如果指定目录不存在就创建：                
                try:
                    if not os.path.exists(
                            os.path.join(
                                os.path.dirname(__file__), 'img/%s' % name)):
                        os.makedirs(
                            os.path.join(
                                os.path.dirname(__file__), 'img/%s' % name))
                    with open(
                            os.path.join(
                                os.path.dirname(__file__),
                                'img/%s/%s.txt' % (name, name)),
                            'w',
                            encoding='utf-8') as f:
                        f.write(content0)
                    for i in range(len(pics)):
                        self.downLoadPic(pics[i], name,
                                         name + '(%s)' % (str(i + 1)))
                except:
                    traceback.print_exc()
                    print('%s、%s存储失败!' % (i, name))
                    with open('erro.txt', 'a', encoding='utf-8') as f:
                        f.write(content0 + '\n\n\n\n\n\n\n')
                zhongyaoDB.dictData = zhongyaoDict
                #zhongyaoDB.executeSQL()
                zhongyaoDB.insertData(zhongyaoDict)
                #time.sleep(random.random())
                print('\n%s、%s的数据保存完毕!\n' % (zyid, name))
                return zhongyaoDict
        else:
            print('呀，这个id=%s的中药你已经在数据库里有了！' % str(i))


if __name__ == '__main__':
    zy = ZhongYao()
    #异步io；
    loop = asyncio.get_event_loop()
    tasks = [zy.getZhongYaoData(i + 1) for i in range(10772)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    '''# 多线程：
    for i in range(10772):
        t = threading.Thread(target=zy.getZhongYaoData, args=(i + 1, ))
        t.start()
        t.join()
    '''