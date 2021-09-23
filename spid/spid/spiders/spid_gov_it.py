import re
import scrapy

import logging

logger = logging.getLogger('scrapy')


class SPIDer(scrapy.Spider):
    name = 'spid.gov.it'
    allowed_domains = ['spid.gov.it']
    start_urls = ['https://www.spid.gov.it/']

    handle_httpstatus_all = True
    handle_httpstatus_list = range(400, 600)

    links = {}
    links_set = set()
    broken = set()
    not_web = {}

    def close(self, spider, reason):
        scrapy.Spider.close(spider, reason)
        # for k,v in self.links.items():
            # logger.info(f"{k}: {', '.join(v)}")

        if self.broken:
            logger.error(f"Broken links: {self.broken}")
        if self.not_web:
            logger.info(f"Found contents not in SGML/JSON format: {self.not_web}")

    def parse(self, response):
        logger.debug(f'Processing: {response.url} ({response.status})')

        if str(response.status)[0] not in ('2', '3'):
            logger.warning(f"Page request failed to {response.url}: {response.status}")
            self.broken.add(response.url)
        elif not self.links.get(response.url):
            self.links[response.url] = []

        links = []
        try:
            _links = response.css('a::attr(href)')
            links = [
                link.get()
                for link in _links
                if link
                and not re.match(r'#|mailto:', link.get())
                and not re.findall("javascript:", link.get(), re.I)
            ]
        except scrapy.exceptions.NotSupported:
            content = response.headers.get('Content-Type', b'').decode()
            logger.warning(f"{response.url} is {content}")
            self.not_web[response.url] = content

        logger.debug(f"Links found in {response.url}: {links}")
        for value in links:
            next_page = response.urljoin(value)
            self.links_set.add(next_page)
            self.links[response.url].append(next_page)
            try:
                #yield from response.follow_all(next_page, self.parse)
                yield scrapy.Request(next_page, callback=self.parse)
            except ValueError as e:
                logger.error(f"{response.url}{value} {e}")
