import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem, CloseSpider
import pandas as pd


class FocusCrawl(CrawlSpider):  #search a given website
    name= "people"
    allowed_domains = ['ethz.ch' ]
    start_urls = [
        'https://css.ethz.ch/en/center/people.html',
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

class GenericCrawl(scrapy.Spider): #load urls from external file, including locations
    name= "skills"
    #overwrite global settings for this spider
    custom_settings = {
                       'ITEM_PIPELINES' : {'SearchTalents.pipelines.JsonWriterPipeline': 201,
                                           'SearchTalents.pipelines.FindKeywords': 200,}}
    def start_requests(self):
        urls = pd.read_json('people_page_link.jl', lines=True)
        location = []
        start_urls = []
        L = len(urls)
        for col in urls:
            for i in range(L):
                if not pd.isna(urls[col][i]):
                    location.append(col)
                    start_urls.append(urls[col][i])
        M = len(start_urls)
        for i in range(M):
            yield scrapy.Request(url=start_urls[i], callback=self.parse, meta={"location" : location[i]} )

    def parse(self, response):
        print(response.url)
        #collect all the paragraphs
        items = response.xpath('//body//text()').getall()
        location = response.meta["location"]

        string_words = ''
        for item in items:
            if item.strip() != '':
                string_words += ' ' + item
        #send the output to the pipeline.py for further processing
        yield {
            location : string_words,
            'url': response.url
        }

class FollowLinks(CrawlSpider):
    name= "links"
    allowed_domains = [
                        'epfl.ch',
                        # 'ethz.ch',
                       #'uu.nl',
#                        'ox.ac.uk',
                                  ]
    start_urls = [
        'https://www.epfl.ch',
#        'https://www.ethz.ch/',
#        'https://www.uu.nl/',
#        'https://www.ox.ac.uk'
        ]
    #overwrite global settings for this spider
    custom_settings = {'CLOSESPIDER_PAGECOUNT' : 20,
                       'ITEM_PIPELINES' : {'SearchTalents.pipelines.JsonWriterPipeline': 201,
                                           'SearchTalents.pipelines.FilterUrl': 200,}}

### FIXME : import the urls from external file ###
    # def start_requests(self):
    #     custom_settings = {'CLOSESPIDER_PAGECOUNT': 25, }
    #
    #     urls = pd.read_json('input_uni_url.jl', lines=True)
    #     location = []
    #     start_urls = []
    #     allowed_domain = []
    #     L = len(urls)
    #     columns = ['start_urls','allowed_domain','location']
    #
    #     for i in range(L):
    #         if not pd.isna(urls['start_urls'][i]):
    #             start_urls.append(urls['start_urls'][i])
    #         if not pd.isna(urls['location'][i]):
    #             location.append(urls['location'][i])
    #         if not pd.isna(urls['allowed_domain'][i]):
    #             allowed_domain.append(urls['allowed_domain'][i])
    #
    #     M = len(start_urls)
    #     for i in range(M):
    #         yield scrapy.Request(url=start_urls[i], callback=self.parse_item, meta={"location" : location[i],
    #                                                                            "start_urls" : start_urls[i],
    #                                                                            "allowed_domain" : allowed_domain[i]})

    #link to personal page of each individual from the main page
    rules = (
        Rule(LinkExtractor(),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
#        location = response.meta["location"]
        yield {
            #"location" : location,
            'url': response.url
        }


