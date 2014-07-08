import scrapy
import bugcrawler.items as items
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy import log


class BugSpider(CrawlSpider):

    name = "bug_crawler"
    allowed_domains = ["launchpad.net"]
    start_urls = [
        "https://bugs.launchpad.net/openstack/"
    ]

    rules = (
        Rule(LinkExtractor(allow=("/\+bug/\d+$"), ),
             callback='parse_item', follow=True),
        Rule(LinkExtractor(allow="/\+bugs.*$", restrict_xpaths="//a[@class='next js-action']",), follow=True)
    )

    def parse_item(self, response):
        # log.msg('Hi, this is an item page! %s' % response.url, level=log.DEBUG)
        # Multiple affects may cause problems
        if "bug" in response.url:
            item = items.BugCrawlerItem()
            item['link'] = response.url
            item['title'] = response.selector.xpath('//h1[@id="edit-title"]/span/text()').extract()
            item['id'] = re.findall("\d+", item['link'])[0]
            description_tmp = response.selector.xpath(
                '//div[@id="edit-description"]/div[@class="yui3-editable_text-text"]/p/text()').extract()
            item['description']= " ".join(description_tmp)
            item['report_time'] = response.selector.xpath('//div[@id="registration"]/span/text()').re('[0-9\-]+')
            item['affects'] = response.selector.xpath(
                '//table[@id="affected-software"]/tbody/tr/td/span/span/a[@class="sprite product"]/text()').extract()
            item['milestone'] = response.selector.xpath('//div[@class="milestone-content"]/a/text()').extract()
            item['importance'] = response.selector.xpath('//div[@class="importance-content"]/span/text()').extract()
            item['status']= response.selector.xpath\
                ('//div[@class="status-content"]/a[contains(@class,"status")]/text()').extract()
            yield item