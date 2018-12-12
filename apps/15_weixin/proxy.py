#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 获取代理 '

__author__ = 'fslong'

import traceback

from config import *
import requests

# 获取代理池的方法有两种，一种是通过数据库，一种是通过api接口，返回值有所不同：
# 本次使用api接口的方式获取，采用每次获取一个代理，如果不好用了就重新获取一个；


def get_proxy_json():
    # 获取单条数据:
    params = '/proxy'
    # 获取多条数据：
    #num = 3
    #params = '/proxies/%s/' % num
    if not API_URL.startswith('http://'):
        url = 'http://'+API_URL+params
    else:
        url = API_URL+params
    response = requests.get(url)
    try:
        dictData = response.json()
        return dictData
    except:
        return False


if __name__ == '__main__':
    print(get_proxy_json())
