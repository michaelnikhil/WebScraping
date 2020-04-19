# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import DropItem, CloseSpider
import re

class FilterText(object):
    #a pipeline for filtering out items which contain certain words in their description

    # put all words in lower case
    words_to_look = ['cybersecurity']

    def process_item(self, item, spider):
        valid=True
        for word in self.words_to_look:
            if word in item['text'].lower():
                valid=True
            else:
                raise DropItem('does not contains "%s"' % word)
        return item

class FindKeywords(object):
    #a pipeline to count the number of keywords in the item

    # put all words in lower case
    # keywords = ['full-stack developer','front-end developer','back-end developer',
    #             'mobile developer','data scientist','designer','product manager']

    keywords = ['law','politics','computer','data','science','economics']

    def process_item(self, item, spider):
        #extract location from the item dict (=key)
        location = list(item.keys())[0]
        #extract the total word count
        word_count =len(item[location].split())
        L = len(self.keywords)

        #prepare output in dict format
        keywords_count = {'location' : location , "url" : item['url'],'word count' : word_count }
        for keyword in self.keywords:
            keywords_count.update({keyword : 0})

        for keyword in self.keywords:
            keywords_count[keyword] = item[location].lower().count(keyword)

        return keywords_count


class FilterUrl(object):
    #a pipeline for filtering out items which contain certain words in their description

    # put all words in lower case
    words_to_look = ['/people' , '/team' , '/members']

    def process_item(self, item, spider):
        valid=False
        for word in self.words_to_look:
            if re.search(word, item['url'].lower()):
                valid=True
        if valid == False:
            raise DropItem()
        return item

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('output.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item