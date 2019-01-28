#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' cspiii（两化融合服务平台）企业能力爬虫 '

__author__ = 'fslong'
__version__ = '0.0.1'

from spider import Spider
import requests,json,csv,re,traceback,random,time

class Cspiii(Spider):
    
    def getData(self):
        self.url = 'http://gltxpd.cspiii.com/Credential/BindData'
        self.data = {'CredentialNumber': '',
                     'CredentialName': '',
                     'State': 1, 
                     'OrgId': -1,
                     'StartTime': '',
                     'EndTime': '',
                     'AreaId': -1,
                     'IndustryID': '',
                     'VersionID': -1,
                     'PageIndex': 1,
                     'PageSize': 50}
        self.error=[]
        for j in range(76):
            print('开始下载第{0}页数据...\n'.format(j+1))
            self.data['PageIndex']=j+1
            def getPage():
                req = requests.post(self.url, data=self.data,headers=self.headers, timeout=15)                
                jsonData=req.json(strict=False)#加了strict=False这个参数可以防止一些json数据格式不严谨导致的错误！
                for i in jsonData['Rows']:
                    if re.match(r'(.*\s*，与)(.*)(能力.*)',i['Range']):
                        i['Range']=re.match('(.*，与)(.*能力)(.*)',i['Range']).group(2)
                    self.results.append(i)
                print('第{0}页数据下载完成，开始存储...\n'.format(j+1))
                self.saveData2Json(self.results,'两化融合通过认证企业')
                self.save2Csv(self.results,'两化融合通过认证企业')
                print('第{0}页数据存储完毕...\n---------------------------------------\n'.format(j+1))
            try:
               getPage()
            except:
                try:
                    getPage()
                except:
                    self.error.append(j)
                    print('第{0}页数据下载失败，请重试...\n---------------------------------------\n'.format(j+1))
                    self.saveData2Json(self.error,'error')
            finally:
                time.sleep(random.randint(3,10))
    

if __name__ == "__main__":
    cspiii=Cspiii()
    cspiii.getData()
    traceback.print_exc()
    print('爬取完毕，请打开/json/error.json文件查看出错的页码！')
    
    

        




    
