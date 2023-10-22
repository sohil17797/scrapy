from typing import Iterable
import scrapy
from scrapy.http import Request


class AudibleSpider(scrapy.Spider):
    name = "audible"
    allowed_domains = ["audible.in"]
    # start_urls = ["https://audible.in/search"]


    # To change User Agent
    def start_requests(self):
        yield scrapy.Request(url="https://audible.in/search", callback=self.parse, 
                       headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"})

    def parse(self, response):
        all_book = response.xpath("//*[@id='center-3']/div/div/div/span[2]/ul/li")

        # yield {
        #     "all_book": all_book,
        # }
        
        for book in all_book:
            # title = book.xpath('.//li[contains(@class, "productListItem")]').get()
            title = book.xpath(".//h3/a/text()").get()
            # title = book.xapth(".//h3[contains(@class, 'bc-heading')]/span/a/text()")
            language = book.xpath(".//li[contains(@class, 'languageLabel')]/span/text()").get()
            language = language.strip() if language else None
            author = book.xpath(".//li[contains(@class, 'authorLabel')]/span/a/text()").get()

            yield {
                "title": title,
                "author": author,
                "language": language,
                # "User-Agent": response.request.headers["User-Agent"],
            }
            
        pagination = response.xpath('//ul[contains(@class, "pagingElements")]')
        next_page_url = pagination.xpath('.//span[contains(@class, "nextButton")]/a/@href').get()
        
        if next_page_url:
            yield response.follow(url=next_page_url, callback=self.parse,
                                  headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"})