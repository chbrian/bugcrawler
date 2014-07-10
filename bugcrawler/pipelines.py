from scrapy.exceptions import DropItem
from bugcrawler.spiders.bug_spider import BugSpider


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, BugSpider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item


class StatusFilterPipeline(object):

    def __init__(self):
        self.invalid_status_list = ['New', 'Incomplete', 'Invalid']

    def process_item(self, item, BugSpider):
        if item['status'] in self.invalid_status_list:
            raise DropItem("Invalid Bug : %s status is %s" % (item['title'], item['status']))
        else:
            return item
