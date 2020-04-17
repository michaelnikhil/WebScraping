# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import DropItem

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


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('output.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item