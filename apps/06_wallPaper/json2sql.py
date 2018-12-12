#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 壁纸json存数据库'

__author__ = 'fslong'
import os
import json
import pymysql
import traceback
import asyncio


class MySQLConnection(object):
    def __init__(self, host='127.0.0.1', port=3306, user='root', passwd='passwd', dbName='WALLPAPER'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbName = dbName

    def executeSQL(self, sql=''):
        if sql == '':
            # 预设sql语句：
            sql = """CREATE TABLE IF NOT EXISTS `wallpaper`(
                    picId INT NOT NULL,# 图片id
                    picName VARCHAR(200),# 图片名称
                    picIntro TEXT,# 图片简介
                    picSize VARCHAR(40),# 图片尺寸
                    picUrl TEXT,# 图片地址，从列表转过来的字符串
                    picPreview TEXT,# 图片预览地址，从列表转过来的字符串
                    picColumn TEXT,# 图片栏目，风景呀美女呀动漫呀什么的
                    picTag TEXT,# 图片便签，一些图片的信息，从列表转过来的字符串
                    picNum INT,# 图片数量，本集合里有几张图片，也就是列表picUrl的长度
                    picType TEXT,# 图片分类，分为三个：手机壁纸、电脑壁纸、美女图片
                    PRIMARY KEY (picId))ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
        db = pymysql.connect(host=self.host, port=self.port,
                             user=self.user, passwd=self.passwd, db=self.dbName, use_unicode=True, charset="utf8")
        cursor = db.cursor()
        # 使用execute()驱动数据库并执行语句：
        try:
            cursor.execute(sql)
            # 提交到数据库执行：
            db.commit()
            # 获取所有记录列表
            #results = cursor.fetchall()
        except:
            traceback.print_exc()
            # 如果发生错误则回滚：
            db.rollback()
        # 关闭数据库链接：
        db.close
        # if results:
        #   return results

    def insertSQLStr(self, values):
        sql = """INSERT INTO wallpaper(picId, picName, picIntro,picSize,picUrl,picPreview,picColumn,picTag,picNum,picType)
        VALUES("%d", "%s", "%s","%s","%s","%s","%s","%s","%d","%s");""" % values
        return sql


if __name__ == '__main__':

    with open(os.path.join(os.path.dirname(__file__), 'wallpaper.json'), 'r', encoding='utf-8') as f:
        wallpaperdict = json.load(f)

    conn = MySQLConnection()
    conn.executeSQL()

    async def saveData2MySQL(conn, i, wallpaperdict):
        print('\n开始存储第%s条数据' % i)
        a = (wallpaperdict[i]['picId'], wallpaperdict[i]['picName'].replace('\"', '\''), wallpaperdict[i]['picIntro'].replace('\"', '\''),
             wallpaperdict[i]['picSize'], wallpaperdict[i]['picUrl'], wallpaperdict[i]['picPreview'],
             wallpaperdict[i]['picColumn'].replace('\"', '\''), str(wallpaperdict[i]['picTag']).replace('\"', '\''), wallpaperdict[i]['picNum'], wallpaperdict[i]['picType'].replace('\"', '\''))
        sql = conn.insertSQLStr(a)
        #sql='SELECT * FROM testTable'
        conn.executeSQL(sql=sql)
        print('第%s条数据存储完毕\n' % i)
    loop = asyncio.get_event_loop()
    m = int(len(wallpaperdict)/2000)
    n = int(len(wallpaperdict) % 2000)
    for j in range(m):
        tasks = [saveData2MySQL(conn, j*2000+i, wallpaperdict)
                 for i in range(2000)]
        loop.run_until_complete(asyncio.wait(tasks))
    tasks = [saveData2MySQL(conn, m*2000+i, wallpaperdict)
             for i in range(2000)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
