#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' shpgx爬虫 '
from spider import Spider

import requests
import json
import random,os,csv
import time


class Shpgx(Spider):
    def getData(self, start=0, wareid=3):
        self.url = 'https://www.shpgx.com/marketstock/dataList'
        data = {'wareid': wareid, 'cd': '', 'starttime	': '',
                'endtime': '', 'start': start, 'length': 25, 'ts': 1546860062759}
        req = requests.post(self.url, data=data,
                            headers=self.headers, timeout=15)
        try:
            jsonData = json.loads(req.content.decode('utf-8'))
        except:
            jsonData = json.loads(req.text)
        for i in jsonData['root']:
            self.results.append(i)
        print(jsonData['current'])
        time.sleep(20*random.random())

    def saveDate(self,filename):
        self.saveData2Json(self.results,filename)
        self.save2Csv(self.results, filename)


if __name__ == "__main__":
    def saveData():
        shpgx = Shpgx()
        for i in range(232):
            shpgx.getData(25*i, 6)
            shpgx.saveDate('shngx_gdq')
        shpgx.results=[]
        for i in range(391):
            shpgx.getData(25*i, 3)
            shpgx.saveDate('shngx_lng')
    def loadOutData():
        path1=os.path.join(os.path.dirname(__file__), 'csv' , 'shngx_gdq_new.csv')
        path2=os.path.join(os.path.dirname(__file__), 'csv' , 'shngx_lng_new.csv')
        path3=os.path.join(os.path.dirname(__file__), 'json' , 'shngx_gdq.json')
        path4=os.path.join(os.path.dirname(__file__), 'json' , 'shngx_lng.json')
        json1=json.load(open(path3))
        json2=json.load(open(path4))
        print(json1[-1])
        print(json2[-1])
        with open(path1,'w+',encoding='utf-8') as f:
            writer =csv.writer(f)
            # 先写入columns_name:
            writer.writerow([i for i in json1[0]])
            for i in json1:
                writer.writerow([i[j] for j in i])
        with open(path2,'w+',encoding='utf-8') as f:
            writer =csv.writer(f)
            # 先写入columns_name:
            writer.writerow([i for i in json2[0]])
            for i in json2:
                writer.writerow([i[j] for j in i])
    loadOutData()

    '''
    shpgx.getData(25*231, 6)
    '''