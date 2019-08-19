# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
from Huobiao.items import HuobiaoItem

class HuoBiaoSpider(CrawlSpider):
    name = 'huo_biao'
    allowed_domains = ['www.huobiao.cn']
    start_urls = ['http://www.huobiao.cn/search/word/%E7%89%A9%E4%B8%9A/']

    rules = (
        Rule(SgmlLinkExtractor(allow=('/detail?id=\w+',)), callback='parse_page', follow=True),
    )
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Referer": "http://www.huobiao.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    }

    # 重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数
    def start_requests(self):
        return [Request("http://www.huobiao.cn/do_login", meta={'cookiejar': 1}, callback=self.post_login)]


        # FormRequeset出问题了
    def post_login(self, response):
        # 登陆成功后, 会调用after_login回调函数
        return [FormRequest.from_response(response,  # "http://www.zhihu.com/login",
                                          meta={'cookiejar': response.meta['cookiejar']},
                                          headers=self.headers,  # 注意此处的headers
                                          formdata={
                                              'phone': '1341953*****',
                                              'password': 'flame314;',
                                              'checkout': 'on'
                                          },
                                          callback=self.after_login,
                                          )]
    def after_login(self, response):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)

    def parse_page(self, response):
        problem = Selector(response)
        item = HuobiaoItem()
        item['title'] =problem.xpath('//span[@class="name"]/text()').extract()
        item['url'] = response.url
        item['name'] = problem.xpath('//span[@class="name"]/text()').extract()


        item['name']
        item['title'] = problem.xpath('//h2[@class="zm-item-title zm-editable-content"]/text()').extract()
        item['description'] = problem.xpath('//div[@class="zm-editable-content"]/text()').extract()
        item['answer'] = problem.xpath('//div[@class=" zm-editable-content clearfix"]/text()').extract()
        return item



