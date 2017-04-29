import scrapy

class QuotesSpider(scrapy.Spider):
    name = "council"

    start_urls = [
            'http://alpineschools.org/schools/'
    ]

    def parse(self, response):
        elementary_links = response.css(
            'div.school-list div.nectar-fancy-ul li a::attr(href)').extract()
        middle_links = response.css(
            'div.middle-list div.nectar-fancy-ul li a::attr(href)').extract()
        high_links = response.css(
            '#ajax-content-wrap > div.container-wrap > div > div > div:nth-child(8) div.nectar-fancy-ul li a::attr(href)').extract()
        for link in elementary_links:
            yield scrapy.Request(link, callback=self.parse_school, meta={"level": "elementary"})
        for link in middle_links:
            yield scrapy.Request(link, callback=self.parse_school, meta={"level": "middle"})
        for link in high_links:
            yield scrapy.Request(link, callback=self.parse_school, meta={"level": "high"})

    def parse_school(self, response):
        data= {'url': response.url,
               'level': response.meta['level']
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
        data['scc_links'] = list(set(scc_links))
        yield data

    def parse_cc(self, response):
        response.css('a::attr(href)').re(r'.*2017.*')
