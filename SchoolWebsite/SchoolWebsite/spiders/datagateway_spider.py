import scrapy
from urlparse import urljoin
class DataGatewaySpider(scrapy.Spider):
    name = "datagateway"
    start_urls = [
            'https://datagateway.schools.utah.gov/AccountabilityReports'
    ]

    def parse(self, response):
        leas = response.css('#selectable-lea > li::attr(data-id)').extract()
        for leaNum in leas:
            yield scrapy.Request(response.url + "?leaNum=" + leaNum,
                                 callback=self.parse_lea)

    def parse_lea(self, response):
        schools = response.css('#selectable-school > li::attr(data-id)').extract()
        for sch in schools:
            yield scrapy.Request(response.url + "&schNum=" + sch,
                                 callback=self.parse_school)
    def parse_school(self, response):
        rel = response.css('#SchoolReportLinks > li:nth-child(1) > a::attr(href)').extract_first()
        url = urljoin(response.url, rel.strip())
        yield scrapy.Request(url, callback=self.parse_school_info)

    def parse_school_info(self, response):
        school_name = response.xpath('//*[@id="pjax-container"]/div[2]/h3/text()').extract_first()
        lea = response.xpath('//*[@id="pjax-container"]/div[2]/h3/small/text()').extract_first()
        principal = response.xpath('//*[@id="pjax-container"]/div[3]/div[1]/dl/dd[1]/text()').extract_first()
        yield {'url': response.url,
               'school_name': school_name,
               'lea': lea,
               'principal': principal,
               'addr1': response.xpath('//*[@id="pjax-container"]/div[3]/div[1]/dl/dd[2]/address/text()[1]').extract_first(),
               'addr2': response.xpath('//*[@id="pjax-container"]/div[3]/div[1]/dl/dd[2]/address/text()[2]').extract_first(),
               'grades': response.xpath('//*[@id="pjax-container"]/div[3]/div[1]/dl/dd[4]/text()').extract_first(),
               'type': response.xpath('//*[@id="pjax-container"]/div[3]/dl/dd[1]/text()').extract_first(),
               'students': response.css('#pjax-container > div.row.school-details > dl > dd:nth-child(4)::text').extract_first(),
               'principals': response.xpath('//*[@id="pjax-container"]/div[3]/dl/dd[3]/text()').extract_first(),
               'counselors': response.xpath('//*[@id="pjax-container"]/div[3]/dl/dd[4]/text()').extract_first(),
               'teachers': response.xpath('//*[@id="pjax-container"]/div[3]/dl/dd[5]/text()').extract_first(),
               'percent endorsed': response.xpath('//*[@id="pjax-container"]/div[3]/dl/dd[6]/text()').extract_first(),
               'percent grad deg': response.xpath('//*[@id="pjax-container"]/div[3]/dl/dd[7]/text()').extract_first(),
               'econ disad': response.xpath('//*[@id="pjax-container"]/div[5]/div[2]/dl/dd[1]/text()').extract_first(),
               'ELL': response.xpath('//*[@id="pjax-container"]/div[5]/div[2]/dl/dd[2]/text()').extract_first(),
               'ethnic minority': response.xpath('//*[@id="pjax-container"]/div[5]/div[2]/dl/dd[3]/text()').extract_first(),
               'special ed': response.xpath('//*[@id="pjax-container"]/div[5]/div[2]/dl/dd[4]/text()').extract_first(),
               }
