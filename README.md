# WebScraping
Search for talents using hard coded web scraping

Program which crawls a predefined list of website, and looks for some basic text information using the Scrapy library.

*to get all the dependencies : pip3 install -r requirements 

*Make sure to change the USER_AGENT in the setting.py : it should be related to the local web browser

*to run from a terminal : scrapy crawl people

*output will be posted to output.jl

*to run from pycharm : create a run configuration using "scrapy" as module name and "crawl people" as parameters
