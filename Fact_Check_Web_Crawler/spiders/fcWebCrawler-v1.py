from gc import callbacks
import scrapy


class fcSpider(scrapy.Spider):
    name = 'boomCrawler-v1'
    allowed_domains = ['https://www.boomlive.in/']
    start_urls = ['https://www.boomlive.in/fact-check/1']

    def start_requests(self):
        urls = [
            'https://www.boomlive.in/fact-check/1',
            'https://www.boomlive.in/fact-check/2'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callbacks=self.parse)

    def parse(self, response):
        page =
