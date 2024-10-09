# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class AgentSpider(scrapy.Spider):
    name = 'agent'
    # allowed_domains = ['airbnb.com']
    start_urls = ['https://www.airbnb.com/rooms/21131821']
    #
    # def start_requests(self):
    #     url = 'https://www.airbnb.com/s/saudi-arabia/homes?refinement_paths%5B%5D=%2Fhomes&query=saudi%20arabia&checkin=2019-03-28&checkout=2019-03-31&adults=1&children=1&guests=1&allow_override%5B%5D=&s_tag=i3UNh5IJ&search_type=PAGINATION'
    #     yield  SplashRequest()

    def parse(self, response):
        # exi
        print(response)
        pass


