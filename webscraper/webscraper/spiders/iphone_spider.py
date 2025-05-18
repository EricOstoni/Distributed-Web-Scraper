import uuid
import scrapy
from ..items import WebscraperItem


class IphoneSpider(scrapy.Spider):
    name = "iphone_spider"
    allowed_domains = ["nabava.net"]
    start_urls = ["https://www.nabava.net/mobiteli?se=1&cod=&cdo="]

    def parse(self, response):

        products = response.css(".product")

        for product in products:

            item = WebscraperItem()

            name = product.css(".product-title::text").get()
            price = product.css(".product__price::text").get()
            link = product.css("a").attrib["href"]

            item["id"] = str(uuid.uuid4())
            item["category"] = "Iphone"
            item["name"] = name.strip() if name else None
            item["price"] = price.strip() if price else None
            item["link"] = f"https://www.nabava.net{link.strip()}" if link else None

            yield item
        next_page = response.css("a.next-page::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
