import json
import re

import scrapy
from scrapy import signals


class URL_Crawler(scrapy.Spider):
    name = 'url_crawler'
    start_urls = ['http://brickset.com/sets/year-2016']
    __urls = {}

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(URL_Crawler, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        spider.max_size = int(spider.max_size)
        return spider

    def spider_closed(self, spider):
        spider.logger.info('Crawling acabado guardando en archivo')
        filtered_urls = {}

        urls = set(self.__urls.keys())  # set(self.getDomain(link) for link in self.__urls.keys())

        for k, v in self.__urls.items():
            intenseccion = v.intersection(urls)
            # if len(intenseccion) != 0:
            filtered_urls[k] = list(intenseccion)

        with open(self.output + '/urls.json', 'w') as f:
            json.dump(filtered_urls, f)

    def parse(self, response):
        PAGE_SELECTOR = "//a/@href"
        URL_SELECTOR = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'

        if len(self.__urls) < self.max_size and self.getDomain(response.url) not in self.__urls:
            links = response.xpath(PAGE_SELECTOR).re(URL_SELECTOR)

            if len(links) != 0:
                filtered_links = set(self.getDomain(link) for link in links)
                self.__urls[self.getDomain(response.url)] = filtered_links
                # links = list(links)

                for link in links:
                    filtered = self.getDomain(link)
                    if filtered not in self.__urls:
                        yield scrapy.Request(
                            url=link,
                            callback=self.parse
                        )

    def getDomain(self, url):
        DOMAIN_SELECTOR = r'[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}'
        return re.search(DOMAIN_SELECTOR, url).group(0)
