import scrapy


class SacScrapyItem(scrapy.Item):
    price = scrapy.Field()
    address = scrapy.Field()
    beds = scrapy.Field()
    baths = scrapy.Field()
    sq_ft = scrapy.Field()
    brokerage = scrapy.Field()

