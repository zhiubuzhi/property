# -*- coding: utf-8 -*-

from property.source.resource import USER_AGENTS
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
import random


class RandomUserAgent(UserAgentMiddleware):

    def process_request(self, request, spider):
        '''

        :param request:
        :param spider:
        :return:
            Requests 对象:停止中间件， request会被重新调度下载
            Response 对象：转交其他中间件process_response
            raise IgnoreRequest 异常：调用Request.errback
        '''
        # print('……下载中间件……')
        # print('下载url：', request.url)
        # print(uagent)
        uagent = random.choice(USER_AGENTS)
        request.headers.setdefault('User-Agent', uagent)