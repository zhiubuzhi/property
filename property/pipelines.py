# -*- coding: utf-8 -*-
import json
import pymysql
from property import settings
from property.items import *


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 连接MySQL数据库将数据写入数据库
class PropertyPipeline(object):

    def __init__(self):
        self.f = open('购房数据.txt', 'a')
        self.f1 = open('租房数据.txt', 'a')
        print('开始记录数据')
        print('连接数据库')
        print(settings.MYSQL_HOST)
        self.connet = pymysql.connect(host=settings.MYSQL_HOST, port=settings.MYSQL_PORT, db=settings.MYSQL_DB,
                                      user=settings.MYSQL_USER, passwd=settings.MYSQL_PASSWD, charset='utf8')
        self.cursor = self.connet.cursor()
        print('已连接数据库')

    def process_item(self, item, spider):
        print('*******************')
        print('这里是管道，将记录数据……')
        if isinstance(item, HouseItem):
            self.f.write(json.dumps(dict(item), ensure_ascii=False) + ',\n')
            self.cursor.execute('INSERT INTO house (address, price, room_type, floors, xiaoqu, area, chanquanniandai, build_year, chaoxiang, first_pay)VALUES(%s, %s, %s, %s, %s, %s, %s %s, %s,%s);'%(item['address'], item['price'], item['room_type'], item['floors'], item['xiaoqu'],item['area'], item['chanquanniandai'], item['chaoxiang'], item['first_pay']))
            self.connet.commit()
        elif isinstance(item, RentItem):
            self.f1.write(json.dumps(dict(item), ensure_ascii=False) + ',\n')
            self.cursor.execute('INSERT INTO house (address, price, pay_way, xiaoqu)VALUES(%s, %s, %s, %s, %s)' % (item['address'],item['price'], item['pay_way'], item['xiaoqu']))
            self.connet.commit()
        return item

    def close_spider(self, spider):
        self.f.close()
        self.f1.close()
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.connet.close()

    def process_item1(self, item, spider):
        pass
