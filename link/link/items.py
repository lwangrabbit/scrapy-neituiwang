# encoding: utf-8

from scrapy.item import Item, Field

#定义存放链接的类
class LinkItem(Item):
    #链接内容
    link = Field()
