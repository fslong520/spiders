#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 使用selenium爬取淘宝 '

__author__ = 'fslong'

import asyncio
import copy
import json
import os
import random
import re
import time
import traceback
from urllib.parse import urlencode

import pymongo
import pyquery
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from config import *


class Taobao (object):
    def __init__(self):
        a = input('默认抓的是美食，是否切换(y/n)?\n')
        if a == 'y':
            self.keyWord = input('请输入要爬取的数据名称：\n')
        else:
            self.keyWord = '美食'
        # 无界面模式：
        options = webdriver.FirefoxOptions()
        options.set_headless()
        # options.add_argument('-headless')
        options.add_argument('--disable-gpu')
        self.browser = webdriver.Firefox(firefox_options=options)
        #self.browser = webdriver.Firefox()
        # 隐式等待，最多加载60，所有元素加载完才执行下一步操作：
        # self.browser.implicitly_wait(60)
        self.wait = WebDriverWait(self.browser, 15)
        self.url = self.searchItem()
        print(self.url)
        self.baseUrl = 'https://s.taobao.com/search?'
        paramsString = self.url.split('?')[1]
        self.params = self.parseParams(paramsString)
        self.params['q'] = self.keyWord
        self.resualts = []
        self.erroItem = []
        # print(self.params)

    # 打开淘宝首页搜索的过程:
    def searchItem(self):
        url = 'https://www.taobao.com'
        self.browser.get(url)
        inputBox = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        for i in self.keyWord:
            inputBox.send_keys(i)
            time.sleep(0.5*random.randint(0, 1))
        inputBox.send_keys(Keys.ENTER)
        # 必须等到页面加载完了才会正常：
        try:
            # 检测是否超时，如果超时就重新加载
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, 'grid')))
        except TimeoutException:
            return self.searchItem()
        finally:
            allPageNumsElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.total')))
            allPageNumsText = allPageNumsElement.text
            print(allPageNumsText)
            try:
                self.allPageNums = re.match(r'(共\s*)(\d+)(\s*页)',
                                            allPageNumsText).group(2)
            except:
                self.allPageNums = 1
            # print(allPageNums)
            #self.allPageNums = 2
            return self.browser.current_url

    # 分析get请求参数值并转换为字典(通过分析加载页面规则的方法需要此函数)：
    def parseParams(self, paramsString):
        params = {}
        for param in paramsString.split('&'):
            params[param.split('=')[0]] = param.split('=')[1]
        return params

    # 将参数解析拼接成真正的url(通过分析加载页面规则的方法需要此函数)：
    def getRealUrl(self):
        return (self.baseUrl+urlencode(self.params))

    # 使用异步方法获取每一页的数据：

    def getItemsByPage(self, pageNum):
        # 通过分析加载页面规则的方法：
        '''
        self.params['s'] = str((pageNum)*44)
        url = self.getRealUrl()
        print(url)
        self.browser.get(url)        
        '''
        # 使用翻页按钮:
        inputPageEle = self.browser.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[3]/div[1]/div[26]/div/div/div/div[2]/input')
        # 清空页码：
        inputPageEle.clear()
        # 输入页码：
        inputPageEle.send_keys(pageNum+1)
        # 实际上就是按了enter键然后翻页：
        inputPageEle.send_keys(Keys.ENTER)
        # 此时已经到了新的页面：
        # 先睡一秒，万一没加载出来呢：
        time.sleep(1)
        # 等待相应元素加载完毕：
        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#mainsrp-p4pBottom'))
        )
        try:
            items = self.browser.find_elements_by_css_selector(
                '#mainsrp-itemlist .items .item')
            for item in items:
                # print(item.text)
                self.parseItem(item, pageNum)
        except:
            traceback.print_exc()

    # 获取所有页面的数据:
    def getAllPageData(self):
        allPageNums = int(self.allPageNums)
        for pageNum in range(1, allPageNums+1):
            print('-----------------\n第%s页\n-----------------' % pageNum)
            self.getItemsByPage(pageNum)
        self.saveDataToJson()

    # 解析数据:
    def parseItem(self, item, pageNum):
        try:
            link = item.find_element(
                By.CSS_SELECTOR, '.title a').get_attribute('href')
            if 'id=' in link:
                productId = re.match(r'(.*id=)(\d+)(&.*)', link).group(2)
                if 'tmall' in link:
                    mall = '天猫'
                else:
                    mall = '淘宝'
                product = {
                    'title': item.find_element(By.CSS_SELECTOR, '.title a').text,
                    'productId': productId,
                    'mall': mall,
                    'image': item.find_element(By.CSS_SELECTOR, '.pic .img').get_attribute('src'),
                    'price': item.find_element(By.CSS_SELECTOR, '.ctx-box .price strong').text,
                    'deal': item.find_element(By.CSS_SELECTOR, '.deal-cnt').text.split('人')[0],
                    'link': item.find_element(By.CSS_SELECTOR, '.title a').get_attribute('href'),
                    'shop': item.find_element(By.CSS_SELECTOR, '.shop').text,
                    'location': item.find_element(By.CSS_SELECTOR, '.location').text,
                }
                print(product)
                # 这里有个坑，需要使用浅拷贝，不然由于mongoDB会自动在字典里加一个_id字段，这会导致json模块dump出错:
                product1 = copy.copy(product)
                self.resualts.append(product1)
                self.saveDataToMongodb(product)
        except:
            self.erroItem.append(item.text)

    # 将数据存到mongodb里:

    def saveDataToMongodb(self, data):
        client = pymongo.MongoClient(host=MONGO_URL, port=MONGO_PORT)
        db = client[MONGO_DB]
        collection = db[self.keyWord]
        collection.insert_one(data)

    def saveDataToJson(self):
        path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), '淘宝%s.json' % self.keyWord)
        with open(path, 'w+', encoding='utf-8') as f:
            json.dump(self.resualts, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    taobao = Taobao()
    taobao.getAllPageData()
    taobao.browser.quit()
    # print('爬取出错的元素有:\n{error}'.format(taobao.erroItem))
