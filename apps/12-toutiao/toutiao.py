#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 今日头条街拍 '

__author__ = 'fslong'

import requests
import pymongo
import os
import traceback
import hashlib
import asyncio
import pymongo


class Toutiao(object):
    def __init__(self):
        self.baseUrl = 'https://www.toutiao.com/search_content/'
        self.params = {
            'offset': '',
            'format': 'json',
            'keyword': '街拍',
            'autoload': 'true',
            'count': 20,
            'cur_tab': 1,
            'from': 'search_tab',
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.18219',
            'Accept-Encoding': 'gzip, deflate, br',

        }
        self.jsons = []
        self.result = []

    def getPage(self, offset):
        self.params['offset'] = offset
        print(self.params)
        try:
            response = requests.get(
                url=self.baseUrl, params=self.params, headers=self.headers)
            if response.status_code == 200:
                return(response.json())
        except requests.ConnectionError as e:
            print(e)

    def getImages(self, dataJson):
        if dataJson.get('data'):
            for item in dataJson.get('data'):
                if item.get('image_list'):
                    images = item.get('image_list')
                    title = item.get('title').split('，')[0].split('：')[0]
                    if title.endswith('街拍'):
                        title = '街拍'+title.split('街拍')[0]
                    self.save2mongo(item)
                    for image in images:
                        url = image.get('url')
                        if url.endswith('_tt'):
                            url = 'http://p9.pstatp.com/large/tuchong.fullscreen/' + \
                                url.split('/')[-1]
                        else:
                            url = 'http:'+url.replace('list', 'large')
                        yield{
                            'image': url,
                            'title': title
                        }
                elif item.get('display'):
                    data = item.get('display')
                    if data.get('items'):
                        data = data.get('items')
                        for image in data:
                            title = image.get('reason').split('，')[
                                0].split('：')[0]
                            if title.endswith('街拍'):
                                title = '街拍'+title.split('街拍')[0]
                            image['title'] = title
                            self.save2mongo(image)
                            yield{
                                'image': image.get('img'),
                                'title': title
                            }

    def saveImage(self, item):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
        path = os.path.join(path, item.get('title'))
        if not os.path.exists(path):
            os.mkdir(path)
        try:
            response = requests.get(item.get('image'), headers=self.headers)
            if response.status_code == 200:                
                file_path = os.path.join(path, '{0}.{1}'.format(hashlib.md5(
                    response.content).hexdigest(), 'jpg'))
                if not os.path.exists(file_path):
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                else:
                    print('好奇怪，这个图片已经下完了！')
        except:
            traceback.print_exc()

    def save2mongo(self, jsonData):
        if jsonData.get('data'):
            mongo = pymongo.MongoClient(host='localhost', port=27017)
            db = mongo['toutiao']
            collector = db['jiepai']
            for data in jsonData.get('data'):
                if collector.find_one(data):
                    print('《%s》的数据已经在数据库中存在！' % data.get('title'))
                else:
                    try:
                        collector.insert_one(data)
                        print('《%s》存储完毕！' % data.get('title'))
                    except:
                        traceback.print_exc()

    async def main(self, offset):
        jsonData = self.getPage(offset)
        self.save2mongo(jsonData)
        for item in self.getImages(jsonData):
            print(item)
            self.saveImage(item)


GROUP_START = 0
GROUP_END = 20

if __name__ == '__main__':
    toutiao = Toutiao()
    loop = asyncio.get_event_loop()
    tasks = [toutiao.main(offset*20)
             for offset in range(GROUP_START, GROUP_END)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
