import scrapy
from ..items import SacScrapyItem

class SacSpider(scrapy.Spider):
    name = "arden_spider_redfin"
    start_urls = [
        f'https://www.redfin.com/city/21251/CA/Arden-Arcade'
        ]
    page_number = 2

    def parse(self, response):

        items = SacScrapyItem()
        redfin_response = response.css('div.bottomV2')

        for rep in redfin_response:
            address = rep.css('a::attr(title)').extract()
            price = rep.css('span.homecardV2Price::text').extract()
            beds = rep.css('div.HomeStatsV2 .stats::text')[0::3].extract()
            baths = rep.css('div.HomeStatsV2 .stats::text')[1::3].extract()
            sq_ft = rep.css('div.HomeStatsV2 .stats::text')[2::3].extract()
            brokerage = rep.css('div.disclaimerV2::attr(title)').extract()

            items['address'] = address
            items['price'] = price
            items['beds'] = beds
            items['baths'] = baths
            items['sq_ft'] = sq_ft
            items['brokerage'] = brokerage

            yield items

        next_page = f'https://www.redfin.com/city/21251/CA/Arden-Arcade/page-{str(self.page_number)}'
        if self.page_number < 5:
            self.page_number += 1
            yield response.follow(next_page, callback=self.parse)
