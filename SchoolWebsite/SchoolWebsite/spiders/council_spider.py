import scrapy
from itertools import chain
class QuotesSpider(scrapy.Spider):
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

    def parse_school(self, response):
        data= {'url': response.url,
               'level': response.meta['level'],
               'name': response.meta['name']
               }
        info = response.css('.header_text::text').extract_first()
        if info:
            info = info.encode('ascii','replace').split(' ? ')
            if len(info) > 0:
                data['address'] = info[0]
            if len(info) > 1:
                data['phone'] = info[1]
            if len(info) > 2:
                data['fax'] = info[2]
        else:
            address = response.css('h4::text').extract_first()
        data['school'] = response.css('title::text').re(r'\w+ \w+')[0]
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
        links = (
            response.css('a::attr(href)').re(r'.*drive.google.*') +
            self.links_insensitive('Agenda', response) +
            self.links_insensitive('Notes', response) +
            self.links_insensitive('Minutes', response) +
            self.links_insensitive('Report', response) +
            self.links_insensitive('Meeting', response) +
            self.links_insensitive('Improvement', response) +
            self.links_insensitive('Plan', response)
            )
        return {
            "url": response.meta['url'],
            "sub-links": links
        }
