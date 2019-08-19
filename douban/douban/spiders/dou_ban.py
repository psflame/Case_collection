# -*- coding: utf-8 -*-
from scrapy import Spider,Request
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from douban.items import DoubanItem
from bs4 import BeautifulSoup


class DouBanSpider(Spider):
    name = 'dou_ban'
    allowed_domains = ['movie.douban.com']
    start_urls = 'https://movie.douban.com/subject/27113517/comments?start={}&limit=20&sort=new_score&status=P'
    num=0
    item = DoubanItem()
    def start_requests(self):
        yield Request(self.start_urls.format(self.num),self.parse_response)

    #spider解析数据
    def parse_response(self, response):

        soup=BeautifulSoup(response.text,'lxml')
        # if soup.state_code!=200:
            # break
        selects=soup.find('div',id='comments').find_all('div')
        for user in selects[:-1]:
            self.item['user_name']=user.find('span',class_='comment-info').a.get_text()
            span_time=user.find('span',class_='comment-time')
            self.item['time']=span_time['title']
            self.item['comment']=user.p.span.get_text()
            yield self.item
        self.num+=20
        yield Request(self.start_urls.format(self.num),self.parse_response)
        # print(selects[0])
        # print(soup)

