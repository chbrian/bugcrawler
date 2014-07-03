import scrapy


class BugSpider(scrapy.Spider):
    name = "bug_crawler"
    allowed_domains = ["launchpad.net"]
    start_urls = [
        "https://bugs.launchpad.net/openstack/",
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)