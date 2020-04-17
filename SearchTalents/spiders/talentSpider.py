import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class FocusCrawl(CrawlSpider):
    name= "people"
    allowed_domains = ['ethz.ch']
    start_urls = [
        'https://css.ethz.ch/en/center/people.html'
    ]

    #link to personal page of each individual from the main page
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths='//a[has-class("default-link")]'),
             callback="parse_item",
             follow=False),)

    def parse_item(self, response):
        #collect all the paragraphs
        items = response.xpath('//p/text()').getall()
        #items = response.xpath('//div[has-class("textimage")/p/text()').getall()
        for item in items:
            if item.strip() != "":
                yield{
                    'text': item.strip()
                }
