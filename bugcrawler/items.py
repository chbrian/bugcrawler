# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BugCrawlerItem(scrapy.Item):

    title = scrapy.Field()
    link = scrapy.Field()
    bug_id = scrapy.Field()
    importance = scrapy.Field()
    affects = scrapy.Field()
    status = scrapy.Field()
    milestone = scrapy.Field()
    description = scrapy.Field()
    report_time = scrapy.Field()
    tags = scrapy.Field()
    bug_life_date_dict = scrapy.Field()
