# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaoquItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #小区ID
    xiaoqu_id = scrapy.Field()
    # 小区均价
    xiaoqu_price = scrapy.Field()
    # 小区地址
    #xiaoqu_address = scrapy.Field()
    #

class RentItem(scrapy.Item):
    '''租房信息'''
    #price
    price = scrapy.Field()
    #pay_way
    pay_way = scrapy.Field()
    # 地址
    address = scrapy.Field()
    pass #需要改
    # 所在小区
    xiaoqu = scrapy.Field()

class HouseItem(scrapy.Item):
    '''购房信息'''

    #地址'
    address = scrapy.Field()
    #总房价
    price = scrapy.Field()
    #房屋户型
    room_type = scrapy.Field()
    #'楼层'
    floors = scrapy.Field()
    #小区
    xiaoqu = scrapy.Field()
    #面积
    area = scrapy.Field()
    # 产权年限
    chanquanniandai= scrapy.Field()
    # 建筑年代
    build_year = scrapy.Field()
    # 朝向
    chaoxiang = scrapy.Field()
    #首付
    first_pay = scrapy.Field()


