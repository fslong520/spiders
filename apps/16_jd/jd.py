#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 使用selenium爬取jd '

__author__ = 'fslong'

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


class JD (object):
    def __init__(self):
        a = input('默认抓的是美食，是否切换(y/n)?\n')
        if a == 'y':
            self.keyWord = input('请输入要爬取的数据名称：\n')
        else:
            self.keyWord = '美食'
        # 无界面模式：
        options = webdriver.FirefoxOptions()
        #options.set_headless()
        # options.add_argument('-headless')
        # 更换头部
        #options.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"')
        #options.add_argument('Cookie="thw=cn; isg=BBoauFiVEgWka56pt2OsAmlsaMD845wvBXgcKiSTQa14l7rRDNvuNeClY-ILXBa9; cna=XtGXFJN/NBgCAX1UPyJUAMqu; t=659ce61312c7c7f57d1b9f260e95cd4c; cookie2=1f0e4e9419ec849b659679ae53bbe3be; v=0; _tb_token_=55178e4d1735a; unb=704407609; uc1=cookie14=UoTYMhjV9Lmr%2Bw%3D%3D&lng=zh_CN&cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&existShop=false&cookie21=VFC%2FuZ9ainBZ&tag=8&cookie15=V32FPkk%2Fw0dUvg%3D%3D&pas=0; sg=09c; _l_g_=Ug%3D%3D; skt=194bfaaa75184bff; publishItemObj=Ng%3D%3D; cookie1=BqeC3SdPLHS9BpRB8Chc8FCzbG2%2BA3IIrbnvwzYFo%2Bw%3D; csg=935aa350; uc3=vt3=F8dByRzIn0iMy1SNN9o%3D&id2=VAFbQx8PkmIJ&nk2=BcN8ljMiosLb59wo&lg2=VT5L2FSpMGV7TQ%3D%3D; existShop=MTU0NDYxMDc3Mw%3D%3D; tracknick=fsl470657570; lgc=fsl470657570; _cc_=WqG3DMC9EA%3D%3D; dnk=fsl470657570; _nk_=fsl470657570; cookie17=VAFbQx8PkmIJ; tg=0; mt=ci=-1_1; enc=r1wo1vjw%2FTEUeBetEStY9REjIxr7yF%2BnYg4Iyfl3PdI3scDWWwRgXhvjMSvnnjjurog12WJWgrXxHLJkuh71tQ%3D%3D"')
        #options.add_argument('--disable-gpu')
        self.browser = webdriver.Firefox(firefox_options=options)
        #　添加代理：
        '''
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.http', proxy['host'])
        profile.set_preference('network.proxy.http_port', int(proxy['port']))
        profile.set_preference(
            'network.proxy.no_proxies_on', 'localhost, 127.0.0.1')
        browser = webdriver.Firefox(
            firefox_profile=profile, firefox_options=options)
        '''
        # self.browser = webdriver.Firefox()
        # 隐式等待，最多加载60，所有元素加载完才执行下一步操作：
        # self.browser.implicitly_wait(60)
        self.wait = WebDriverWait(self.browser, 15)
        self.url = self.searchItem()
        print(self.url)
        self.baseUrl = 'https://s.jd.com/search?'
        paramsString = self.url.split('?')[1]
        self.params = self.parseParams(paramsString)
        self.params['q'] = self.keyWord
        self.resualts = []
        self.erroItem = []
        # print(self.params)

    # 打开jd首页搜索的过程:
    def searchItem(self):
        url = 'https://www.jd.com/'
        self.browser.get(url)
        inputBox = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#key'))
        )
        for i in self.keyWord:
            inputBox.send_keys(i)
            time.sleep(0.5*random.randint(0, 1))
        inputBox.send_keys(Keys.ENTER)
        # 必须等到页面加载完了才会正常：
        try:
            # 检测是否超时，如果超时就重新加载
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, 'dropdown')))
        except TimeoutException:
            return self.searchItem()
        finally:
            allPageNumsElement = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.p-skip > em:nth-child(1) > b:nth-child(1)')))
            allPageNumsText = allPageNumsElement.text
            print(allPageNumsText)
            try:
                self.allPageNums = int(allPageNumsText)
                self.allPageNums=3
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
        inputPageEle = self.browser.find_element_by_css_selector(
            '.p-skip input')
        # 清空页码：
        inputPageEle.clear()
        # 输入页码：
        inputPageEle.send_keys(pageNum+1)
        # 实际上就是按了enter键然后翻页：
        inputPageEle.send_keys(Keys.ENTER)
        # 此时已经到了新的页面：
        # 先睡1秒，万一没加载出来呢(主要是图片比较慢)：
        time.sleep(1)        
        # 等待相应元素加载完毕：
        self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#J_goodsList'))
        )
        try:
            items = self.browser.find_elements_by_css_selector(
                '#J_main #J_goodsList .gl-warp .gl-item .gl-i-wrap')
            down=0
            for item in items:
                # 然后把滚动条往下拖，只有拖动了进度条，才能加载完全，这里使用的是运行js脚本的方法：                
                self.browser.execute_script('window.scrollBy(0,100)')
                time.sleep(1)
                # print(item.text)
                self.parseItem(item, pageNum)
        except:
            traceback.print_exc()

    # 获取所有页面的数据:
    def getAllPageData(self):
        allPageNums = int(self.allPageNums)
        for pageNum in range(0, allPageNums):
            print('-----------------\n第%s页\n-----------------' % (pageNum+1))
            self.getItemsByPage(pageNum)
        self.saveDataToJson()

    # 解析数据:
    def parseItem(self, item, pageNum):
        try:
            link = item.find_element(
                By.CSS_SELECTOR, '.p-name a').get_attribute('href')            
            try:
                productId = re.match(r'(.*item.jd.com/)(\d+)(\..*)', link).group(2)
            except:
                productId=item.find_element(By.CSS_SELECTOR, '.promo-words').get_attribute('id')                

            product = {
                'title': item.find_element(By.CSS_SELECTOR, '.p-name a em').text,
                'productId': productId,
                'image': item.find_element(By.CSS_SELECTOR, '.p-img a img').get_attribute('src'),
                'price': item.find_element(By.CSS_SELECTOR, '.p-price strong i').text,
                'commit': item.find_element(By.CSS_SELECTOR, '.p-commit strong a').text.split('+')[0],
                'link': link,
                'shop': item.find_element(By.CSS_SELECTOR, '.p-shop a').text,
            }
            print(product)
            # 这里有个坑，需要使用浅拷贝，不然由于mongoDB会自动在字典里加一个_id字段，这会导致json模块dump出错:
            product1 = copy.copy(product)
            self.resualts.append(product1)
            #self.saveDataToMongodb(product)
        except:
            #traceback.print_exc()
            self.erroItem.append(item.text)

    # 将数据存到mongodb里:

    def saveDataToMongodb(self, data):
        client = pymongo.MongoClient(host=MONGO_URL, port=MONGO_PORT)
        db = client[MONGO_DB]
        collection = db[self.keyWord]
        collection.insert_one(data)

    def saveDataToJson(self):
        path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'jd%s.json' % self.keyWord)
        with open(path, 'w+', encoding='utf-8') as f:
            json.dump(self.resualts, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    jd = JD()
    jd.getAllPageData()
    jd.browser.quit()
    # print('爬取出错的元素有:\n{error}'.format(jd.erroItem))
