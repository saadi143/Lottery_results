# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LotteryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    draw_number = scrapy.Field()
    draw_1 = scrapy.Field()
    draw_2 = scrapy.Field()
    draw_3 = scrapy.Field()
    draw_4 = scrapy.Field()
    draw_5 = scrapy.Field()
    draw_6 = scrapy.Field()
    draw_7 = scrapy.Field()
    maker_result = scrapy.Field()
    match = scrapy.Field()
    star = scrapy.Field()
    prize = scrapy.Field()
    winner = scrapy.Field()
    total = scrapy.Field()

class hotpicks(scrapy.Item):
    date = scrapy.Field()
    match = scrapy.Field()
    prize = scrapy.Field()
    winner = scrapy.Field()
    total = scrapy.Field()
