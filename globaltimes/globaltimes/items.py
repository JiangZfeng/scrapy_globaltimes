# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class GlobaltimesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    article_level_one = scrapy.Field()
    article_level_two = scrapy.Field()
    pub_time = scrapy.Field()
    content = scrapy.Field()
    pass