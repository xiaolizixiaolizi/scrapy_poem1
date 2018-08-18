# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymysql import cursors
from twisted.enterprise import adbapi


class GushiwenPipeline(object):
    def process_item(self, item, spider):
        return item


# database/poem  数据库/表
class GuShiWenTwistPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'gushiwen',
            'charset': 'utf8',
            'cursorclass':cursors.DictCursor

        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql_insert = None

    @property
    def sql_insert(self):
        if not self._sql_insert:
            self._sql_insert = '''
            insert into poem(id,author,title,content)
            values (null,%s,%s,%s)
            '''
            return  self._sql_insert
        return self._sql_insert #第一次为none 第二次就不是None


    def process_item(self,item,spider):
        defer=self.dbpool.runInteraction(self.insert_item,item)
        defer.addErrback(self.handle_error,item)

        return  item
    def insert_item(self,cursor,item): #传入cursor
        cursor.execute(self.sql_insert,(
            item['author'],item['title'],item['content']
        ))
    def handle_error(self,error,item): #传入error
        print('=='*10)
        print(error)
        print('=='*10)




