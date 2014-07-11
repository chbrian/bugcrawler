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


class AffectsFilterPipeline(object):
    def __init__(self):
        # At current stage, we only focus on IaaS level and production period. So we exclude Tempest, Triple, Fuel,
        # heat, and other projects.
        self.valid_affect_list = [
            'OpenStack Dashboard (Horizon)',
            'OpenStack Object Storage (swift)',
            'oslo',
            'OpenStack Compute (nova)',
            'Ceilometer',
            'Cinder',
            'oslo.messaging',
            'Keystone',
            'Glance',
            'neutron']

    def process_item(self, item, BugSpider):
        len_affects = len(item['affects'])
        len_status = len(item['status'])
        len_milestone = len(item['milestone'])
        len_importance = len(item['importance'])
        if len_affects == 1:
            if item['affects'][0] not in self.valid_affect_list:
                raise DropItem("Irrelevant affect of %s" % item['title'])
        else:
            new_affects_list = []
            new_status_list = []
            new_milestone_list = []
            new_importance_list = []
            if (len_affects == len_status or len_status == 0) \
                    and (len_affects == len_milestone or len_milestone == 0) \
                    and (len_affects == len_importance or len_importance == 0):
                for i in item['affects']:
                    if i in self.valid_affect_list:
                        index = item['affects'].index(i)
                        new_affects_list.append(item['affects'][index])
                        if not len_status == 0:
                            new_status_list.append(item['status'][index])
                        if not len_milestone == 0:
                            new_milestone_list.append(item['milestone'][index])
                        if not len_importance == 0:
                            new_importance_list.append(item['importance'][index])

                if not new_affects_list:
                    raise DropItem("Irrelevant affect of %s" % item['title'])
                else:
                    item['affects'] = new_affects_list
                    item['status'] = new_status_list
                    item['milestone'] = new_milestone_list
                    item['importance'] = new_importance_list
            else:
                flag = 0
                for i in item['affects']:
                    if i in self.valid_affect_list:
                        flag = 1
                if flag == 0:
                    raise DropItem("Irrelevant affect of %s" % item['title'])
        return item