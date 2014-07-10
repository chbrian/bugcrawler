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


class FormatPipeline(object):

    def __init__(self):
        pass

    def process_item(self, item, BugSpider):
        for field in item:
            if type(item[field]) == str:
                item[field] = item[field].strip()
            elif type(item[field]) == list:
                item[field] = [i.strip('\n').strip() for i in item[field]]
            else:
                pass
        return item


class StatusFilterPipeline(object):

    def __init__(self):
        self.invalid_status_list = ['New', 'Incomplete', 'Invalid']

    def process_item(self, item, BugSpider):
        for i in item['status']:
            if i not in self.invalid_status_list:
                return item
        raise DropItem("Invalid status of %s" % item['title'])
