#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 处理搜狗相关 '

__author__ = 'fslong'
import re
import traceback

import pyquery
import requests
from requests.exceptions import ConnectionError

from proxy import get_proxy_json


class Sogou(object):
    def __init__(self):
        self.keyword = '风景'
        self.proxy = None
        self.params = {
            'query': self.keyword,
            'type': 2,
            'page': 1,
            'ie': 'utf8'
        }
        self.headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
            'Cookie': 'ABTEST=3|1537341435|v1; IPLOC=CN6103; SUID=C088737C6E2F940A000000005BA1F7FB; SUID=C088737C7C20940A000000005BA1F7FB; weixinIndexVisited=1; SUV=00F54F787C7388C05BA1F7FBB63C4681; sct=1; SNUID=87C03B3B474D3E737A3E586C48AC6632; JSESSIONID=aaaL09B4R2-J34B2T0Bvw; ppinf=5|1537341861|1538551461|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTUlODYlQUYlRTQlQjglOTYlRTklQkUlOTl8Y3J0OjEwOjE1MzczNDE4NjF8cmVmbmljazoyNzolRTUlODYlQUYlRTQlQjglOTYlRTklQkUlOTl8dXNlcmlkOjQ0Om85dDJsdU5xUG15Uk5TOGZzTlBuNDFMX2FwaE1Ad2VpeGluLnNvaHUuY29tfA; pprdig=bXK01pDEFtuo_x3gIOHkCncJt_knA9BaoR_uRcOyXJ2Dfi_f8HcxAOsA6G_mqJMXjjscS3B6_1QwA-1WCIxZ558axPHdn_Z5n9cU278RPjUA2vf_Fc-eN1SrvdAlsg999aceemD5avxSUDa7LkoYzmoKbwpR3PtepWRfXTMB_mA; sgid=07-35022335-AVuhibaXuGFMe55hfqause5M; ppmdig=15373418620000001c8d1a55e273e79339b74566ac466db2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Host': 'weixin.sogou.com',
            'Upgrade-Insecure-Requests': '1',

        }
        self.base_url = 'http://weixin.sogou.com/weixin'
        self.news_url = []
        self.count = 0
        self.max_count = 20

    def get_page(self, page, count=1):
        if count >= self.max_count:
            print('第%s页请求错误次数过多!' % page)
            return False
        self.params['page'] = page
        try:
            if self.proxy:
                proxies = {
                    'http': 'http://'+self.proxy['ip']+':'+self.proxy['port'],
                }
                response = requests.get(
                    url=self.base_url, params=self.params, headers=self.headers, allow_redirects=False, proxies=proxies)
            else:
                response = requests.get(
                    url=self.base_url, params=self.params, headers=self.headers, allow_redirects=False)
            print(response.status_code)
            if response.status_code == 200:
                try:
                    html = response.content.decode('utf-8')
                except:
                    traceback.print_exc()
                    html = response.text
                finally:
                    pq = pyquery.PyQuery(html)
                    # print(pq('.yh').text())
                    return pq
            if response.status_code == 302:
                self.proxy = get_proxy_json()
                if self.proxy:
                    print('使用代理', self.proxy)
                    return self.get_page(page, count)
                else:
                    return False
        except ConnectionError:
            count += 1
            self.proxy = get_proxy_json()
            return self.get_page(page, count)

    def get_total_num(self):
        htmlPQ = self.get_page(1)
        if htmlPQ:
            text = htmlPQ('.mun').text()
            text = text.replace(',', '')
            numText = re.match(r'(.*约)(\d+)(条.*)', text).group(2)
            # print(text)
            try:
                num = int(numText)
                return(num)
            except:
                traceback.print_exc()
                return False
        else:
            return False

    def get_all_pages_num(self):
        totle_num = self.get_total_num()
        if totle_num:
            all_pages_num = totle_num//10+1
            return all_pages_num
        else:
            return False

    def get_all_pages(self):
        #all_pages_num = self.get_all_pages_num()
        all_pages_num = 1  # 爬几页意思意思就是了
        for i in range(all_pages_num):
            pagePQ = self.get_page(i+1)
            if pagePQ:
                items = pagePQ('.news-list li').items()
                for item in items:
                    text_box = item('.txt-box')
                    news_title = text_box('h3').text()
                    if news_title:
                        url = text_box('h3 a').attr('href')
                        self.count += 1
                        if not url.startswith('http'):
                            if url.startswith('//'):
                                url = 'http:'+url
                            else:
                                url = 'http://'+url
                    self.news_url.append(
                        {'id': self.count, 'title': news_title, 'url': url})
            else:
                return False


if __name__ == '__main__':
    sogou = Sogou()
    sogou.get_all_pages()
    for i in sogou.news_url:
        print(i)
