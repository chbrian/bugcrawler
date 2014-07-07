import scrapy
import bugcrawler.items as items
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector


class BugSpider(CrawlSpider):
    name = "bug_crawler"
    allowed_domains = ["launchpad.net"]
    start_urls = [
        "https://bugs.launchpad.net/openstack/"
    ]

    rules = (
        Rule(LinkExtractor(allow=("/[0-9]+"), ),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        hxs = HtmlXPathSelector(response)
        if response.url:
            item = items.BugcrawlerItem()
            item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
            item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
            item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
            yield item