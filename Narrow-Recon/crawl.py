from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import ast
from scrapy import Item
from scrapy import Field


class UrlItem(Item):
    url = Field()


class Spider(CrawlSpider):
    name = 'time'
    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls').split(',')
        allow = []
        if self.start_urls[0][:5] == "https":
            allow.append(self.start_urls[0][8:])
            self.allowed_domains  = allow
        else:
            allow.append(self.start_urls[0][7:])
            self.allowed_domains  = allow
    rules = (
        Rule(LinkExtractor(), callback='parse_url'),
    )

    def parse_url(self, response):
        item = UrlItem()
        item['url'] = response.url

        return item