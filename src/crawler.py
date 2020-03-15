import re

import scrapy
from scrapy import signals
from tinydb import TinyDB, Query


class URL_Crawler(scrapy.Spider):
    name = 'url_crawler'
    start_urls = ['http://brickset.com/sets/year-2016']
    __db = None

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(URL_Crawler, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        spider.max_size = int(spider.max_size)
        return spider

    def spider_closed(self, spider):
        spider.logger.info('Crawling Cerrando DB')

        self.__db.close()

    def spider_opened(self, spider):
        spider.logger.info('Crawling, Iniciando DB')
        self.__db = TinyDB(self.output + '/urls2.json', default_table='links')
        self.__db.purge()

    def parse(self, response):
        PAGE_SELECTOR = "//a/@href"
        URL_SELECTOR = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'

        url = Query()

        if len(self.__db) < self.max_size and not self.__db.contains(url.domain == self.getDomain(response.url)):
            links = response.xpath(PAGE_SELECTOR).re(URL_SELECTOR)

            # Al crear un set nos aseguramos que cada link solo aparece una vez
            filtered_links = set(self.getDomain(link) for link in links)
            self.__db.insert({
                'domain': self.getDomain(response.url),
                'links': list(filtered_links)
            })

            for link in links:
                filtered = self.getDomain(link)
                if not self.__db.contains(url.domain == self.getDomain(filtered)):
                    yield scrapy.Request(
                        url=link,
                        callback=self.parse
                    )

    def getDomain(self, url):
        DOMAIN_SELECTOR = r'[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}'
        return re.search(DOMAIN_SELECTOR, url).group(0)
