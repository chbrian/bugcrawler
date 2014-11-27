import scrapy
import bugcrawler.items as items
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy import log


class BugSpider(CrawlSpider):

    name = "bug_crawler"
    allowed_domains = ["launchpad.net"]

    # testing url
    start_urls = ["https://bugs.launchpad.net/openstack-ci/+bug/1010621"]

    # real-case url
    """
    start_urls = []
    d = range(0, 8800, 75)
    for i in d:
        abc = "https://bugs.launchpad.net/openstack/+bugs?orderby=-importance&memo=#&start=#"
        start_urls.append(abc.replace('#', str(i)))
    """
    rules = (
        Rule(LinkExtractor(allow=("/\+bug/\d+$"), ),
             callback='parse_item', follow=True),
        #Rule(LinkExtractor(restrict_xpaths="//a[@class='next js-action' and contains(@strong, 'Next')]",), follow=True),
        #Rule(LinkExtractor(allow=("/\+bugs\?orderby=-importance&memo=\d+&start=\d+$"), ),
        #     follow=True)
    )

    def parse_item(self, response):
        # log.msg('Hi, this is an item page! %s' % response.url, level=log.DEBUG)
        # Multiple affects may cause problems
        item = items.BugCrawlerItem()
        item['link'] = response.url
        item['id'] = re.findall("\d+", item['link'])[0]
        item['title'] = response.selector.xpath('//h1[@id="edit-title"]/span/text()').extract()
        description_tmp = response.selector.xpath(
            '//div[@id="edit-description"]/div[@class="yui3-editable_text-text"]/p/text()').extract()
        #description_tmp = 3  #[i.strip('/n').strip() for i in description_tmp]
        item['description'] = " ".join(description_tmp)
        item['report_time'] = response.selector.xpath('//div[@id="registration"]/span/@title').extract()
        item['affects'] = response.selector.xpath(
            '//table[@id="affected-software"]/tbody/tr/td/span/span/a[@class="sprite product"]/text() '
            '| //table[@id="affected-software"]/tbody/tr/td/span[@class="sprite milestone"]/../a/text()').extract()
        item['milestone'] = response.selector.xpath('//div[@class="milestone-content"]/a/text()').extract()
        item['importance'] = response.selector.xpath('//div[@class="importance-content"]/span/text()').extract()
        item['status']= response.selector.xpath(
            '//div[@class="status-content"]/a[contains(@class,"status")]/text()').extract()
        item['tags'] = response.selector.xpath('//div[@id="bug-tags"]/span[@id="tag-list"]/a/text()').extract()

        yield item