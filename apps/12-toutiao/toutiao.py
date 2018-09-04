#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 今日头条街拍 '

__author__ = 'fslong'

import requests
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
        self.result=[]

    def getPage(self, offset):
        self.params['offset'] = offset
        print(self.params)
        try:
            response = requests.get(url=self.baseUrl, headers=self.headers)
            if response.status_code == 200:
                self.jsons.append(response.json())
        except requests.ConnectionError as e:
            print(e)
    
    def getImages(self):
        for json in self.jsons:
            if json.get('data'):
                for item in json.get('title'):
                    images=item.get('')
                

