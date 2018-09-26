#! /user/bin/evn python
# -*- coding: utf-8 -*-

from property.source.resource import PROXIES
import random

class RandomProxy:

    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        request.meta['proxy'] = 'http://%s' % proxy

