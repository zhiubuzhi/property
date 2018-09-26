#! /user/bin/evn python
# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy.selector import Selector, HtmlXPathSelector
from property.items import *
import platform

# 如果解决windows命令窗口打印乱码或报错
if platform.system():
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')


# 获取广州二手房购房信息和租房信息
class TenementSpider(scrapy.Spider):
    name = 'tenement'
    allowed_domains = ['gz.58.com']
    start_urls = ['https://gz.58.com/xiaoqu/']
    hasurl = {}

    def parse(self, response):
        '''
        解析小区信息
        获取详情页面
        :param response:
        :return:
        '''
        url_list = Selector(response=response).xpath('//tbody//li[@class="tli1"]//a/@href').extract()
        # 获取某页下的小区url
        for url in url_list:
            print('准备进入小区获取信息url:%s' % url)
            yield Request(
                url=url,
                callback=self.deal
            )

        # 寻找下一页
        next_xiaoqu_url = Selector(response=response).xpath('//a[@class = "next"]/@href').extract_first()
        if next_xiaoqu_url:
            yield Request(
                url=next_xiaoqu_url,
                callback=self.parse
            )

    def deal(self, response):
        print('小区url：', response.url)
        # 检测是否访问过度频繁,在没有代理的情况，结束方法
        if self.check(response): return

        xiaoqu_price = Selector(response=response).xpath('//div[@class="price-container"]//span/text()').extract_first()
        room_urls = Selector(response=response).xpath('//a[@class="fy-link"]/@href').extract()
        print('开始获取该小区的租房和购房详细信息')
        print('小区均价：', xiaoqu_price)
        yield Request(url='https:' + room_urls[0], callback=self.deal_selledroom)
        yield Request(url='https:' + room_urls[1], callback=self.deal_rent_room)

    def deal_selledroom(self, response):
        # 检测是否访问过度频繁
        if self.check(response): return
        print('获取二手房url列表:%s' % response.url)
        room_urls = Selector(response=response).xpath('//a[@class="t"]/@href').extract()
        for url in room_urls:
            if TenementSpider.url_to_md5(url) not in self.hasurl:
                print('获取购房url:', url)
                yield Request(url=url, callback=self.house)

        # 寻找下一页
        next_url = response.css('a.next::attr(href)').extract_first()
        if next_url:
            yield Request(
                url=next_url,
                callback=self.deal_selledroom
            )

    def deal_rent_room(self, response):
        # 检测是否访问过度频繁
        print('获取以下url租房列表%s' % response.url)
        if self.check(response): return

        room_urls = Selector(response=response).xpath('//td[@class="t"]/a[1]/@href').extract()

        for url in room_urls:
            if TenementSpider.url_to_md5(url) not in self.hasurl:
                yield Request(url=url, callback=self.rent_room)

        # 寻找下一页
        next_url = response.css('a.next::attr(href)').extract_first()
        if next_url:
            yield Request(
                url=next_url,
                callback=self.deal_rent_room
            )

    def house(self, response):
        # 检测是否访问过度频繁
        if self.check(response): return

        print('-------------打印购房信息--------------')
        print(response.url)
        try:
            if '星球' in response.text:
                print('被反爬了')
            mes = Selector(response=response).xpath(
                '//div[@class="general-item-wrap"]//span[@class="c_000"]/text()').extract()
            price = Selector(response=response).xpath(
                '//*[@id="generalExpense"]/div/ul[1]/li[1]/span[2]/text()').extract_first().strip()
            first_pay = Selector(response=response).xpath(
                '//*[@id="generalExpense"]//ul[@class="general-item-right"]/li/span[2]/text()').extract_first().strip()
            room_type = mes[1].strip()
            area = mes[2].strip()
            chaoxiang = mes[3].strip()
            floors = mes[4].strip()
            chanquanniandai = mes[6].strip()
            build_year = mes[7].strip()
            xiaoqu = Selector(response=response).xpath('//h3[@class="xiaoqu-name"]/a/text()').extract_first().strip()
            address = Selector(response=response).xpath(
                '//ul[@class="xiaoqu-desc"]//span[@class="c_333"]//a[@class="c_333"]/text()').extract_first().strip()

            print('地址', address)
            print('总房价', price)
            print('房屋户型', room_type)
            print('楼层', floors)
            print('小区', xiaoqu)
            print('面积', area)
            print('产权年限', chanquanniandai)
            print('建筑年代', build_year)
            print('朝向', chaoxiang)
            print('首付', first_pay)
            item = HouseItem()
            item['address'] = address
            item['price'] = price
            item['room_type'] = room_type
            item['floors'] = floors
            item['xiaoqu'] = xiaoqu
            item['chanquanniandai'] = chanquanniandai
            item['build_year'] = build_year
            item['chaoxiang'] = chaoxiang
            item['first_pay'] = first_pay

            key = TenementSpider.url_to_md5(response.url)
            self.hasurl[key] = response.url
            return item

        except IndexError as e:
            print(e)
            print(response.url)

    def rent_room(self, response):
        # 检测是否访问过度频繁
        if self.check(response): return
        print('-------------打印租房信息----------------')
        print(response.url)
        if 'pinpaigongyu' in response.url:
            print('**************品牌公寓*************')
            price = response.xpath('//span[@class="price"]/text()').extract_first()
            mes = response.xpath('//h2/text()').extract_first()
            import re
            mes_list = re.split(re.compile('【|】| '), mes)
            pay_way = mes_list[1]
            address = mes_list[2]
            xiaoqu = mes_list[3]
        else:
            print('***********其他出租公寓***********')
            price = Selector(response=response).xpath(
                '//div[@class ="house-desc-item fl c_333"]//div[@class="house-pay-way f16"]//b[@class="f36 strongbox"]/text()').extract_first().strip()
            mes = Selector(response=response).xpath(
                '//div[@class="house-desc-item fl c_333"]//ul//li/span[2]/text()').extract()
            a_lis = Selector(response=response).xpath(
                '//div[@class="house-desc-item fl c_333"]//ul//li//a[@class="c_333 ah"]/text()').extract()
            pay_way = Selector(response=response).xpath('//ul[@class="f14"]/li[1]/span[2]/text()').extract_first()
            xiaoqu = a_lis[0].strip()
            address = a_lis[1].strip()
            for i in range(len(mes)):
                print(i, mes[i])

        print('price', price)
        print('pay_way', pay_way)
        print('地址', address)
        print('所在小区', xiaoqu)
        item = RentItem()
        item['price'] = price
        item['pay_way'] = pay_way
        item['xiaoqu'] = xiaoqu
        item['address'] = address

        key = TenementSpider.url_to_md5(response.url)
        self.hasurl[key] = response.url
        return item

    def check(self, response):
        if '频繁' in response.text:
            print("提示访问过于频繁，被发现了。")
            return 1

    @staticmethod
    def url_to_md5(url):
        import hashlib
        return hashlib.md5().update(bytes(url, encoding='utf-8'))
