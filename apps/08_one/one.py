#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' one-一个 '

__author__ = 'fslong'

import asyncio
import base64
import os
import time
import traceback

import pyquery
import requests

from spider import Spider


class One(Spider):
    def getOneUrls(self):
        self.url = 'http://www.wufazhuce.com'
        req = requests.get(self.url, headers=self.headers)
        onePQs = pyquery.PyQuery(req.text)
        self.oneUrls = []
        # print(onePQs)
        for i in onePQs('.item > a').items():
            self.oneUrls.append(i.attr.href)
        return (self.oneUrls)

    async def getDetails(self, url):
        req = requests.get(url, headers=self.headers)
        onePQ = pyquery.PyQuery(req.text)
        picUrl = onePQ('.one-imagen > img').attr.src
        picId = onePQ('.one-titulo').text()
        picStory = onePQ('.one-cita').text()
        pubDate = onePQ('.dom').text() + '-' + onePQ('.may').text().split(
            ' ')[0] + '-' + onePQ('.may').text().split(' ')[1]
        self.results.append({
            'picId': picId,
            'picStory': picStory,
            'pubDate': pubDate,
            'picUrl': picUrl
        })
        self.downLoadPic(picUrl, picId)
        print('\n%s\n'%picStory)
        self.saveData2Json(self.results, 'one')

        return self.results


if __name__ == '__main__':
    one = One()
    one.getOneUrls()
    loop = asyncio.get_event_loop()
    tasks = [one.getDetails(url) for url in one.oneUrls]
    loop.run_until_complete(asyncio.wait(tasks))
