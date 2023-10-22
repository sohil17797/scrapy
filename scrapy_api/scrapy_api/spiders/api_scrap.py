import scrapy
import json

class ApiScrapSpider(scrapy.Spider):
    name = "api_scrap"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/api/quotes?page=1"]

    def parse(self, response):
        json_response = json.loads(response.body)
        quotes = json_response.get('quotes')
        for quote in quotes:
            yield {
                "author": quote.get('author').get('name'),
                "text": quote.get('text'),
                "quote": quote.get('tags'),
            }
        # print(quotes)
        has_next = json_response.get('has_next')
        if has_next:
            next_page = json_response.get('page') + 1
            yield scrapy.Request(url=f"https://quotes.toscrape.com/api/quotes?page={next_page}", callback=self.parse)
