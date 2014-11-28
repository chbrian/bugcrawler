import bugcrawler.items as items
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy import log


class BugActivitySpider(CrawlSpider):

    name = "bug_activity"
    allowed_domains = ["launchpad.net"]

    # testing url
    start_urls = ["https://bugs.launchpad.net/python-cinderclient/+bug/1028684/+activity"]

    # real-case url
    """
    start_urls = []
    d = range(0, 8800, 75)
    for i in d:
        abc = "https://bugs.launchpad.net/openstack/+bugs?orderby=-importance&memo=#&start=#"
        start_urls.append(abc.replace('#', str(i)))
    """
    rules = (
        Rule(LinkExtractor(allow=("/\+bug/\d+/+activity$"), ),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = items.BugActivityItem()
        item['link'] = response.url
        item['bug_id'] = re.findall("\d+", item['link'])[0]
        bug_life = {}
        time_list = response.selector.xpath('//td[contains(text(), ": status")]/../td[1]/text()').extract()
        status_list = response.selector.xpath('//td[contains(text(), ": status")]/../td[5]/text()').extract()
        affect_list = response.selector.xpath('//td[contains(text(), ": status")]/text()').extract()
        affect_list = [affect.split(':')[0] for affect in affect_list]
        report_time = response.selector.xpath('//td[contains(text(), " 	added bug")]/..td[1]/text()').extract()
        bug_life.update({"New": report_time})
        for i in range(len(status_list)):
            bug_life.update({status_list[i]: time_list[i]})
        yield item