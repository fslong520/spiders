
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 处理json文件 '

__author__ = 'fslong'


import ast  # 用于将字符串转为字典
import pymysql
import os
import json
import threading
import asyncio
import re


if __name__ == '__main__':
    path = os.path.dirname(__file__)
    with open(os.path.join(path, 'jsons/all/enterdesk123.json'), 'r', encoding='utf-8') as f:
        wallPaperDict = json.load(f)
    wallPaperList = []
    # 添加enterdeskjson的函数

    def appendEnterdeskPic(wallPaperList, picDict):
        if picDict['picIntro'].startswith('内容简介'):
            picDict['picIntro'] = picDict['picIntro'].replace('内容简介', '')
        wallPaperList.append(picDict)
        print('%s、%s' % (wallPaperList[-1]['picId'], picDict['picName']))
    for i in wallPaperDict:
        t = threading.Thread(target=appendEnterdeskPic, args=(
            wallPaperList, i['result']))
        t.start()
        t.join()
    maxId = 0
    for i in range(len(wallPaperList)-1):
        if wallPaperList[i]['picId'] < wallPaperList[i+1]['picId']:
            maxId = wallPaperList[i+1]['picId']
    with open(os.path.join(path, 'jsons/all/netbian.json'), 'r', encoding='utf-8') as f:
        wallPaperDict = json.load(f)

    print(maxId)

    # 添加enterdeskjson的函数

    async def appendNetBianPic(wallPaperList, picDict, maxId):
        picDict['clumnName'] = picDict['clumnName'].split('壁纸')[0]
        if '美女' in picDict['clumnName']:
            picColumn = ['美女图片', '美女壁纸']
        elif '手机' in picDict['clumnName']:
            picColumn = ['手机壁纸', '手机']
        else:
            picColumn = ["电脑壁纸", picDict['clumnName']]
        wallPaperList.append({
            'picId': maxId+picDict['picId'],
            'picName': picDict['picName'],
            'picIntro': picDict['picName'],
            'picSize': picDict['picSize'],
            'picUrl': [picDict['picUrl']],
            'picPreview': [picDict['picPreview']],
            'picColumn': picColumn,
            'picTag': [picDict['clumnName']],
            'picNum': 1,
        })
        print('%s、%s' % (wallPaperList[-1]['picId'], picDict['picName']))
    # 创建异步io进程池
    loop = asyncio.get_event_loop()
    # 创建任务列表
    tasks = [appendNetBianPic(wallPaperList, i, maxId) for i in wallPaperDict]
    # 执行任务
    loop.run_until_complete(asyncio.wait(tasks))
    # 关闭任务池
    loop.close()
    maxId = 0
    for i in range(len(wallPaperList)-1):
        if wallPaperList[i]['picId'] < wallPaperList[i+1]['picId']:
            maxId = wallPaperList[i+1]['picId']

    with open(os.path.join(path, 'jsons/all/wallpapersite.json'), 'r', encoding='utf-8') as f:
        wallPaperDict = json.load(f)
    # 添加wallpapersite的图片
    for i in wallPaperDict:
        for j in wallPaperDict[i]['data']:
            picDict = wallPaperDict[i]['data'][j]
            print(picDict['picName'])
            wallPaperList.append({
                'picId': maxId+int(i.split('page')[1])*12+int(j.split('pic')[1]),
                'picName': picDict['picName'],
                'picIntro': picDict['picName'],
                'picSize': picDict['picUrl'][0]['size'],
                'picUrl': [picDict['picUrl'][0]['url']],
                'picPreview': [picDict['picUrl'][0]['url'].replace(picDict['picUrl'][0]['size'], '360x360')],
                'picColumn': ["电脑壁纸", picDict['picColumn']],
                'picTag': picDict['picTag'],
                'picNum': 1,
            })
            print('%s、%s' % (wallPaperList[-1]['picId'], picDict['picName']))
    for i in range(len(wallPaperList)):
        if len(wallPaperList[i]['picColumn']) == 5:
            wallPaperList[i]['picColumn'].remove(
                wallPaperList[i]['picColumn'][0])
            wallPaperList[i]['picColumn'].remove(
                wallPaperList[i]['picColumn'][-1])
            wallPaperList[i]['picColumn'].remove(
                wallPaperList[i]['picColumn'][-1])
        if len(wallPaperList[i]['picColumn']) == 3:
            wallPaperList[i]['picColumn'].remove(
                wallPaperList[i]['picColumn'][2])
        for j in range(len(wallPaperList[i]['picColumn'])):
            if wallPaperList[i]['picColumn'][j] == 'Abstract' or wallPaperList[i]['picColumn'][j] == 'Others'or wallPaperList[i]['picColumn'][j] == 'Typography':
                wallPaperList[i]['picColumn'][j] = '其他'
            elif wallPaperList[i]['picColumn'][j] == 'Animals' or wallPaperList[i]['picColumn'][j] == '动物壁纸':
                wallPaperList[i]['picColumn'][j] = '动物'
            elif wallPaperList[i]['picColumn'][j] == 'Anime' or wallPaperList[i]['picColumn'][j] == '动漫' or wallPaperList[i]['picColumn'][j] == '动漫壁纸':
                wallPaperList[i]['picColumn'][j] = '动漫卡通'
            elif wallPaperList[i]['picColumn'][j] == 'Automotive':
                wallPaperList[i]['picColumn'][j] = '汽车'
            elif wallPaperList[i]['picColumn'][j] == 'Celebrations' or '月日历壁纸' in wallPaperList[i]['picColumn'][j] or wallPaperList[i]['picColumn'][j] == 'Celebrities':
                wallPaperList[i]['picColumn'][j] = '节日'
            elif wallPaperList[i]['picColumn'][j] == 'Creative Graphics':
                wallPaperList[i]['picColumn'][j] = '创意'
            elif wallPaperList[i]['picColumn'][j] == 'Cute':
                wallPaperList[i]['picColumn'][j] = '可爱'
            elif wallPaperList[i]['picColumn'][j] == 'Fantasy':
                wallPaperList[i]['picColumn'][j] = '奇幻'
            elif wallPaperList[i]['picColumn'][j] == 'Flowers':
                wallPaperList[i]['picColumn'][j] = '植物'
            elif wallPaperList[i]['picColumn'][j] == 'Games':
                wallPaperList[i]['picColumn'][j] = '游戏'
            elif wallPaperList[i]['picColumn'][j] == 'Lifestyle':
                wallPaperList[i]['picColumn'][j] = '生活'
            elif wallPaperList[i]['picColumn'][j] == 'Love':
                wallPaperList[i]['picColumn'][j] = '爱情'
            elif wallPaperList[i]['picColumn'][j] == 'Military':
                wallPaperList[i]['picColumn'][j] = '军事'
            elif wallPaperList[i]['picColumn'][j] == 'Minimal':
                wallPaperList[i]['picColumn'][j] = '创意'
            elif wallPaperList[i]['picColumn'][j] == 'Movies':
                wallPaperList[i]['picColumn'][j] = '影视'
            elif wallPaperList[i]['picColumn'][j] == 'Music':
                wallPaperList[i]['picColumn'][j] = '汽车'
            elif wallPaperList[i]['picColumn'][j] == 'Nature':
                wallPaperList[i]['picColumn'][j] = '自然'
            elif wallPaperList[i]['picColumn'][j] == 'Photography':
                wallPaperList[i]['picColumn'][j] = '摄影'
            elif wallPaperList[i]['picColumn'][j] == 'Space' or wallPaperList[i]['picColumn'][j] == 'World':
                wallPaperList[i]['picColumn'][j] = '风景'
            elif wallPaperList[i]['picColumn'][j] == 'Sports':
                wallPaperList[i]['picColumn'][j] = '运动'
            elif wallPaperList[i]['picColumn'][j] == 'Technology':
                wallPaperList[i]['picColumn'][j] = '科技'
            elif wallPaperList[i]['picColumn'][j] == 'TV Series':
                wallPaperList[i]['picColumn'][j] = '影视'
    i = 0
    picNum = 0
    for j in wallPaperList:
        i += 1
        j['picId'] = i
        j['picType'] = j['picColumn'][0]
        j['picColumn'] = j['picColumn'][1]
        picNum += j['picNum']
    print('\n合并完毕\n一共%s组%s张图片' % (i, picNum))
    
    with open(os.path.join(path, 'wallpaper.json'), 'w', encoding='utf-8') as f:
        json.dump(wallPaperList, f, ensure_ascii=False)
    with open(os.path.join(path, 'wallpaper.json'), 'r', encoding='utf-8') as f:
        wallPaperList=json.load(f)
    for i in wallPaperList[1]:
        print('%s:%s'%(i,wallPaperList[1][i]))