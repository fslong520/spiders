#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' cspiii爬虫 '
from spider import Spider
import requests
import xlwt
import json
import re
import time
import random
import os
import csv


class Cspiii(Spider):

    # 获取当前数据：

    def getOrgIncreaseSituationData(self, ids=-1, ctype='Country'):
        self.url = 'http://gltxpd.cspiii.com/External/GetOrgIncreaseSituationData'
        data = {'ids': ids, 'ctype': ctype}
        req = requests.post(self.url, data=data,
                            headers=self.headers, timeout=15)
        return self.page2json(req)

        # 评定年度增长情况：
    def getAllOrgImplementationSituationData(self, ids=-1, ctype='Country'):
        self.url = 'http://gltxpd.cspiii.com/External/GetAllOrgImplementationSituationData'
        data = {'ids': ids, 'ctype': ctype}
        req = requests.post(self.url, data=data,
                            headers=self.headers, timeout=15)
        return self.page2json(req)

    # 获取各省id：

    def getOrgData(self):
        self.url = 'http://gltxpd.cspiii.com/External/GetOrgData'
        data = {}
        req = requests.post(self.url, data=data,
                            headers=self.headers, timeout=15)
        return self.page2json(req)

    # 获取各省两化融合数据：
    def getProvinceData(self):
        data = []
        for i in self.getOrgData()['data']:
            # print(i['OrganizationId'])
            ids = int(i['OrganizationId'])
            temp = self.getOrgIncreaseSituationData(ids, 'Province')
            for i in self.getAllOrgImplementationSituationData(ids, 'Province')['alldata']:
                temp['data'].append(i)
            data.append(temp)
        self.saveData2Json(data, '各省两化融合数据')
        return data

    # 获取各行业id：

    def getIndBaseData(self):
        self.url = 'http://gltxpd.cspiii.com/External/GetIndBaseData'
        data = {'GetIndBaseData': ''}
        req = requests.post(self.url, data=data,
                            headers=self.headers, timeout=15)
        return self.page2json(req)

    # 获取两化融合各行业数据：

    def industryData(self):
        data = []
        for i in self.getIndBaseData()['data']:
            # print(i['OrganizationId'])
            ids = int(i['ID'])
            temp = self.getOrgIncreaseSituationData(ids, 'PIndustry')
            for i in self.getAllOrgImplementationSituationData(ids, 'PIndustry')['alldata']:
                temp['data'].append(i)
            data.append(temp)
        self.saveData2Json(data, '各行业两化融合数据')
        return data

    # 获取央企ID：

    def getYQData(self):
        self.url = 'http://gltxpd.cspiii.com/External/GetYQData'
        data = {}
        req = requests.post(self.url, data=data,
                            headers=self.headers, timeout=15)
        return self.page2json(req)

    # 获取两化融合各央企数据：

    def yqData(self):
        data = []
        for i in self.getYQData()['data']:
            # print(i['OrganizationId'])
            ids = int(i['ID'])
            temp = self.getOrgIncreaseSituationData(ids, 'Enterprise')
            for i in self.getAllOrgImplementationSituationData(ids, 'Enterprise')['alldata']:
                temp['data'].append(i)
            data.append(temp)
        self.saveData2Json(data, '央企两化融合数据')
        return data

    # 获取两化融合全国数据：

    def qgData(self):
        data = []
        temp = self.getOrgIncreaseSituationData()
        for i in self.getAllOrgImplementationSituationData()['alldata']:
            temp['data'].append(i)
        data.append(temp)
        self.saveData2Json(data, '全国两化融合数据')
        return data

    # 获取重庆两化融合服务机构数据：

    def getBindConsulationAgent(self):
        self.url = 'http://yhkzt.cspiii.com/External/BindConsulationAgent'
        data = {'AgentName': '', 'ProvinceID': 2465, 'Level': -1, 'KeyIndustry': -
                1, 'KeyCity': -1, 'AgentType': '', 'PageIndex': 1, 'PageSize': 10}
        req = requests.post(self.url, data=data,
                            headers=self.headers, timeout=15)
        dicts = self.page2json(req)
        # for i in range(10):
        for i in range(int(dicts['Total'])//10+1):
            if i != 0:
                data = {'AgentName': '', 'ProvinceID': 2465, 'Level': -1, 'KeyIndustry': -
                        1, 'KeyCity': -1, 'AgentType': '', 'PageIndex': i+1, 'PageSize': 10}
                req = requests.post(self.url, data=data,
                                    headers=self.headers, timeout=15)
                dicts['Rows'].append(self.page2json(req))
                # time.sleep(10*random.random())
        self.saveData2Json(dicts, '重庆两化融合服务机构')
        return dicts

    def set_style(self, name, height, bold=False):
        style = xlwt.XFStyle()  # 初始化样式

        font = xlwt.Font()  # 为样式创建字体
        font.name = name  # 'Times New Roman'
        font.bold = bold
        font.color_index = 4
        font.height = height

        # borders= xlwt.Borders()
        # borders.left= 6
        # borders.right= 6
        # borders.top= 6
        # borders.bottom= 6

        style.font = font
        # style.borders = borders

        return style

    # 将各省数据从json存到excel

    def saveJson2csvexcel(self):
        path = os.path.join(os.path.dirname(__file__), 'json', '各省两化融合数据.json')
        self.createDir('csv')
        path1 = os.path.join(os.path.dirname(
            __file__), 'xls', '各省两化融合数据.xls')
        with open(path, 'r', encoding='utf-8') as f:
            jsonData = json.load(f)
            print(jsonData)
        self.createDir('xls')
        f = xlwt.Workbook()
        sheet1 = f.add_sheet('各省两化融合数据', cell_overwrite_ok=True)
        row0 = ['序号', '省份', '总启动评定', '总通过评定',
                '2016年', '', '2017年', '', '2018年', '', '2019年', '']
        row1 = ['', '', '', '', '启动评定', '通过评定', '启动评定',
                '通过评定', '启动评定', '通过评定', '启动评定', '通过评定']

        for i in range(len(row0)):
            sheet1.write(0, i, row0[i], self.set_style(
                'Times New Roman', 220, True))
        for i in range(len(row1)):
            sheet1.write(1, i, row1[i], self.set_style(
                'Times New Roman', 220, True))
        
        j = 2
        for i in jsonData:
            data = [j-1, i['data'][0]['Xtitle'], i['data'][0]['Qnum'], i['data'][0]['Tnum'],
                    i['data'][2]['Year1'], i['data'][3]['Year1'],
                    i['data'][2]['Year2'], i['data'][3]['Year2'],
                    i['data'][2]['Year3'], i['data'][3]['Year3'],
                    i['data'][2]['Year4'], i['data'][3]['Year4']
                    ]
            for k in range(len(data)):
                sheet1.write(j, k, data[k], self.set_style('Times New Roman', 220, False))
            
            j+=1
        f.save(path1)


if __name__ == "__main__":
    cspiii = Cspiii()
    # cspiii.yqData()
    # cspiii.industryData()
    # cspiii.getProvinceData()
    # cspiii.qgData()
    # cspiii.getBindConsulationAgent()
    cspiii.saveJson2csvexcel()
