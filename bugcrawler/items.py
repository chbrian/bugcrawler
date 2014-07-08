# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BugCrawlerItem(scrapy.Item):
    # define the fields for your item here like:

    title = scrapy.Field()
    link = scrapy.Field()
    id = scrapy.Field()
    importance = scrapy.Field()
    affects = scrapy.Field()
    status = scrapy.Field()
    milestone = scrapy.Field()
    description = scrapy.Field()
    report_time = scrapy.Field()