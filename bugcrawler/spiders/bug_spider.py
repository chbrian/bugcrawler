import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class BugSpider(scrapy.Spider):
    name = "bug_crawler"
    allowed_domains = ["launchpad.net"]
    start_urls = [
        "https://bugs.launchpad.net/openstack/"
    ]

    rules = (
        Rule(LinkExtractor(allow=('https://bugs.launchpad.net/[a-z]*/+bug/[0-9]+')))
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)

        item = scrapy.Item()
        item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        return item