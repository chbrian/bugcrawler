
import bugcrawler.items as items
import datetime
import re
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy import log


class BugSpider(CrawlSpider):

    name = "bug_crawler"
    allowed_domains = ["launchpad.net"]

    # testing url
    start_urls = ["https://bugs.launchpad.net/openstack/"]

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
        item['bug_id'] = re.findall("\d+", item['link'])[0]
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

        # Processing bug life date
        # Collect bug life and its corresponding affect
        bug_life_status = ["Incomplete", "Confirmed", "Triaged", "In Progress", "Fix Committed", "Fix Released",
                    "Invalid", "Opinion", "Won't Fix"]
        bug_life_time_dict = {}
        bug_life_affect_dict = {}
        for life in bug_life_status:
            # xpath has a bug that path can't include tbody.
            try:
                time_list = response.selector.xpath(
                    '//table[@class="bug-activity"]/tr/td[contains(text(), %s)]/../../../../div[1]/span/text()' % life).extract()
                time_list = [datetime.datetime.strptime(date.split()[1], "%Y-%m-%d") for date in time_list]
                bug_life_time_dict.update({life: time_list})
                affect_list = response.selector.xpath(
                    '//table[@class="bug-activity"]/tr/td[contains(text(), %s)]/../../tr[1]/td/text()' % life).extract()
                affect_list = [affect.split()[2][:-1] for affect in affect_list]
                bug_life_affect_dict.update({affect_list: affect_list})
            except:
                log.msg("No bug life of %s in report %s." % (life, item['bug_id']), logLevel=log.DEBUG)

        # choose the minimal bug time of each life, that is the date bug changes to this status
        bug_life_date_dict = {}
        for status in bug_life_status:
            affect_set = set(bug_life_affect_dict.get(status))
            for affect in affect_set:
                time_list = []
                for j in range(len(bug_life_affect_dict.get(status))):
                    if affect == bug_life_affect_dict.get(status)[j]:
                        time = bug_life_time_dict.get(status)[j]
                        time_list.append(time)
                time = min(time_list)
            bug_life_date = {affect, time}
            bug_life_date_dict.update({status: bug_life_date})

        item["bug_life_date_dict"] = bug_life_date_dict

        yield item