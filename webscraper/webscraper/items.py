# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebscraperItem(scrapy.Item):
    id = scrapy.Field()
    category = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()

    pass
