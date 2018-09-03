#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 下载文件测试 '

__author__ = 'fslong'

import asyncio
import base64
import os
import sys
import time
import traceback

import pyquery
import requests

from spider import Spider
if __name__ == '__main__':
    url = input('请输入下载文件的地址：\n')
    spider = Spider()
    spider.saveData(url)
