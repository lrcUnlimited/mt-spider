__author__ = 'li'
# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from meituan_spider.items import MeituanSpiderItem


class MeiTuanSpider(CrawlSpider):
    name = "mtfood"
    allowed_domains = ["meituan.com"]
    start_urls = [
        'http://cd.meituan.com/category/meishi/all/page1?mtt=1.index%2Fdefault%2Fpoi.0.0.icbbj8kl'
    ]

    rules = [
        # get food detail in page response
        Rule(LinkExtractor(allow=r"http://www\.meituan\.com/shop/[0-9]{1,}#smh:bdw$",
                           restrict_xpaths='//a[@class="poi-tile__head"]'), callback="parse_detail"),
        # get next page link and return page response
        Rule(LinkExtractor(allow="/category/meishi/all/page\d{1,}\?mtt=*", restrict_xpaths=('//li[@class="next"]')),
             follow=True)
    ]

    def parse_detail(self, response):
        item = MeituanSpiderItem()
        sel = Selector(response)
        item['url'] = response.url
        shop_name = sel.xpath('//div[@class="fs-section__left"]/h2/span[@class="title"]/text()').extract()[0]
        shop_address = sel.xpath(
            '//div[@class="fs-section__left"]/p[@class="under-title"][1]/span[@class="geo"]/text()').extract()[0]
        item['phone'] = sel.xpath('//div[@class="fs-section__left"]/p[@class="under-title"][2]/text()').extract()[0]

        item['point'] = sel.xpath(
            '//div[@class="fs-section__right"]/div[@class="info"]/div[1]/span[@class="biz-level"]/strong/text()').extract()[
            0]
        shop_type = sel.xpath('//div[@class="fs-section__right"]/div[@class="info"]/div[2]/a/text()').extract()[0]
        item['consume_num'] = sel.xpath('//div[@class="counts"]/div[1]/span[@class="num"]/text()').extract()[0]
        item['judge_num'] = sel.xpath('//div[@class="counts"]/div[2]/a/text()').extract()[0]
        item['shopName'] = shop_name
        item['address'] = shop_address
        item['type'] = shop_type
        print item

        yield item









        









