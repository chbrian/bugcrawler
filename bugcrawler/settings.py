# -*- coding: utf-8 -*-

# Scrapy settings for bugcrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'bugcrawler'

SPIDER_MODULES = ['bugcrawler.spiders']
NEWSPIDER_MODULE = 'bugcrawler.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bugcrawler (+http://www.yourdomain.com)'