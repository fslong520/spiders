#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' selenium相关 '

__author__ = 'fslong'

import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def example():

    # 配置文件地址
    profile_directory = '/home/fslong/.mozilla/firefox/83l1qwct.default'
    # 加载配置配置
    profile = webdriver.FirefoxProfile(profile_directory)
    browser = webdriver.Firefox(profile)    
    browser.get('https://www.baidu.com')
    # 无界面模式：
    options = webdriver.FirefoxOptions()
    options.set_headless()
    # options.add_argument('-headless')
    options.add_argument('--disable-gpu')
    browserDriver=webdriver.Firefox(firefox_options=options)
    browserDriver.get('https://www.baidu.com')

    '''
    inputFirst = browser.find_element_by_id('q')
    inputSecond = browser.find_element_by_name('q')
    inputThird = browser.find_element_by_css_selector('#q')
    inputForth = browser.find_element_by_xpath('//*[@id="q"]')
    inputFifth = browser.find_element(By.ID, 'q')
    print(inputFirst, '\n', inputSecond, '\n',
          inputThird, '\n', inputForth, '\n', inputFifth)
    
    lis = browser.find_elements_by_css_selector('.service-bd li')
    for i in lis:
        print('%s = %s' % ('class', i.get_attribute('class')))
        print('%s = %s' % ('text', i.text))
    browser.close()
    '''



if __name__ == '__main__':
    example()
