import scrapy
from itertools import chain
from .council_spider import SCCSpider
class GraniteSpider(SCCSpider):
    name = "granite"
    start_urls = [
            'http://www.graniteschools.org/schools/'
    ]


    def link_school(self, selector, response, level):
        links = response.css(selector)
        results = zip(links.css('::text').extract(),
                      links.css('::attr(href)').extract())
        for text, link in results:
            yield scrapy.Request(link, callback=self.parse_school,
                                 meta={"level": level,
                                       "name": text})

    def parse(self, response):
        yield scrapy.Request(response.xpath('//a[contains(.,"elementary")]/@href').extract_first(),
                             callback = self.parse_schools, meta={"level": "elementary"})
        yield scrapy.Request(response.xpath('//a[contains(.,"junior")]/@href').extract_first(),
                             callback = self.parse_schools, meta={"level": "middle"})
        yield scrapy.Request(response.css('a::attr(href)').re(r'.*senior.*')[0],
                             callback = self.parse_schools, meta={"level": "high"})

    def parse_schools(self, response):
        for link in response.css('td.column-1 a'):
            name = link.css('::text').extract_first()
            yield scrapy.Request(link.css('::attr(href)').extract_first(),
                                 callback= self.parse_school, meta={
                                     "level": response.meta['level'],
                                     "name": name
                                 })
