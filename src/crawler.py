import json
import re

import numpy as np
import scipy
import scrapy
from scipy.sparse import lil_matrix
from scrapy import signals


def getDomain(url):
    DOMAIN_SELECTOR = r'[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}'
    return re.search(DOMAIN_SELECTOR, url).group(0)


def limpiarUrls(urls):
    domains = set(urls.keys())
    filtered = {}

    for domain, links in urls.items():
        filtered[domain] = list(links.intersection(domains))

    return filtered


class URL_Crawler(scrapy.Spider):
    name = 'url_crawler'
    start_urls = ['http://brickset.com/sets/year-2016']
    __urls = {}

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(URL_Crawler, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        spider.max_size = int(spider.max_size)
        return spider

    def spider_closed(self, spider):
        spider.logger.info('Crawling Cerrando')

        matrix = lil_matrix((len(self.__urls), len(self.__urls)), dtype=np.bool)

        urls = limpiarUrls(self.__urls)
        urls2int = {}

        for domain, links in urls.items():
            if domain not in urls2int:
                urls2int[domain] = len(urls2int)

            for link in links:
                if link not in urls2int:
                    urls2int[link] = len(urls2int)

                i = urls2int[domain]
                j = urls2int[link]

                matrix[i, j] = 1

        scipy.sparse.save_npz(self.output + '/matrix.npz', matrix.tocsr())
        with open(self.output + '/urls.json', 'w') as f:
            json.dump(urls2int, f)

    def spider_opened(self, spider):
        spider.logger.info('Crawling, Iniciando')

    def parse(self, response):
        PAGE_SELECTOR = "//a/@href"
        URL_SELECTOR = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        domain = getDomain(response.url)
        if len(self.__urls) < self.max_size and domain not in self.__urls:

            # Al crear un set nos aseguramos que cada link solo aparece una vez
            links = set(response.xpath(PAGE_SELECTOR).re(URL_SELECTOR))

            filtered_links = set(getDomain(link) for link in links)
            self.__urls[domain] = filtered_links

            for link in links:
                filtered = getDomain(link)
                if filtered not in self.__urls:
                    yield scrapy.Request(
                        url=link,
                        callback=self.parse
                    )
