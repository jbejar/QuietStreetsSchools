import scrapy
from itertools import chain
import logging

class SCCSpider(scrapy.Spider):
    def parse_school(self, response):
        logging.info("S " + response.url)
        data= {'url': response.url,
               'level': response.meta['level'],
               'name': response.meta['name']
               }
        scc_links = response.css('a::attr(href)').re(r'.*scc.*')
        scc_links += response.css('a::attr(href)').re(r'.*council.*')
        scc_links += response.xpath('//span[contains(.,"SCC")]/../@href').extract()
        scc_links += response.xpath('//a[contains(.,"SCC")]/@href').extract()
        scc_links += response.xpath('//a[contains(.,"Council")]/@href').extract()
        scc_links = [link for link in list(set(scc_links)) if 'student-council' not in link]
        for link in scc_links:
            yield scrapy.Request(link, callback=self.parse_cc,
                                     meta={'url':response.url})
        data['scc_links'] = scc_links
        yield data

    def links_insensitive(self, word, response):
        return (response.xpath('//a[contains(.,"%s")]/@href' % word).extract() +
            response.xpath('//a[contains(.,"%s")]/@href' % word.lower()).extract()
            )
    def parse_cc(self, response):
        for link in response.xpath('//a[contains(.,"CLICK HERE")]/@href').extract():
            yield scrapy.Request(link, callback=self.parse_cc,
                                 meta={'url': response.meta['url'] })
        links = list(set(
            response.css('a::attr(href)').re(r'.*drive.google.*') +
            response.css('a::attr(href)').re(r'.*docs.google.*') +
            response.css('a::attr(href)').re(r'.*[Mm]inutes.*') +
            response.css('a::attr(href)').re(r'.*[Rr]eport.*') +
            response.css('a::attr(href)').re(r'.*[Aa]genda.*') +
            response.css('a::attr(href)').re(r'.*[Cc]ouncil.*') +
            self.links_insensitive('Agenda', response) +
            self.links_insensitive('Notes', response) +
            self.links_insensitive('Minutes', response) +
            self.links_insensitive('Report', response) +
            self.links_insensitive('Meeting', response) +
            self.links_insensitive('Improvement', response) +
            self.links_insensitive('Plan', response)
            ))
        url = response.meta['url']
        for link in links:
            for year in range(2013, 2018):
                if str(year) in link or str(year)[2:] in link:
                    yield {'url': url,
                           year: True}
            if link.endswith('pdf') or link.endswith('docx') or link.endswith('doc'):
                continue
            yield scrapy.Request(link, callback=self.parse_doc,
                                 meta={'url':url})
        yield {
            "url": url,
            "sub-links": links
        }

    def parse_doc(self, response):
        data = {'url': response.meta['url']}
        for year in range(2013, 2018):
            if str(year) in response.body:
                data[year] = True
        yield data

class QuotesSpider(SCCSpider):
    name = "council"
    start_urls = [
            'http://alpineschools.org/schools/'
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
        gen = chain(
        self.link_school('div.school-list div.nectar-fancy-ul li a', response,
                    "elementary"),
        self.link_school('div.middle-list div.nectar-fancy-ul li a',
                         response, "middle"),
        self.link_school('#ajax-content-wrap > div.container-wrap > div > div > div:nth-child(8) div.nectar-fancy-ul li a', response,
                    "high"))
        for g in gen:
            yield g
