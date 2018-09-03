#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' 从字典存到数据库的函数 '

__author__ = 'fslong'
__version__ = '0.0.2'

import pymysql
import traceback


# 定义存储数据库的类
class MySQLConnection(object):
    def __init__(self,
                 host='127.0.0.1',
                 port=3306,
                 user='root',
                 passwd='passwd',
                 dbName='TESTDB',
                 tabName='testTable',
                 dictData={'id': 1}):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbName = dbName
        self.dictData = dictData
        self.tabName = tabName

    # 执行提交sql语句的函数：
    def executeSQL(self, sql=''):
        if sql == '':
            # 生成预设sql语句：
            sql = """CREATE TABLE IF NOT EXISTS `%s`(""" % self.tabName
            keys=[]
            for i in self.dictData:
                keys.append(i)
            for i in range(len(keys)):
                if i ==0:
                    sql += """%s VARCHAR(40) , """ % keys[i]
                else:
                    sql += """%s TEXT , """ % keys[i]
            sql += """PRIMARY KEY (`%s`))ENGINE=InnoDB DEFAULT CHARSET=utf8;"""%keys[0]

        db = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            db=self.dbName,
            use_unicode=True,
            charset="utf8")
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

    # 插入数据的函数：
    def insertData(self, dictData={'id': 1}):
        self.dictData = dictData
        # 先看下表结构有没有生成，没有生成就生成一下:
        self.executeSQL()
        # 拼接sql语句：
        sql = """INSERT INTO %s (""" % (self.tabName, )
        for i in self.dictData:
            sql += """%s,""" % i
        sql = sql[0:-1] + """)""" + """VALUES("""
        for i in self.dictData:
            sql += """\"%s\",""" % dictData[i]
        sql = sql[0:-1] + """);"""
        self.executeSQL(sql)
