# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field

# meituan data bind to shopdetail tb
class MeituanSpiderItem(Item):
    shopName = Field()
    point = Field()
    type = Field()
    address = Field()
    phone = Field()
    consume_num = Field()
    judge_num = Field()
    url = Field()
    repost = Field()



