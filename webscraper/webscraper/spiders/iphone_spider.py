import uuid
import scrapy
from ..items import WebscraperItem


class IphoneSpider(scrapy.Spider):
    name = "iphone_spider"
    allowed_domains = ["nabava.net", "svijet-medija.hr"]

    start_urls = [
        "https://www.nabava.net/mobiteli?se=1&cod=&cdo=",
        "https://www.svijet-medija.hr/gg/88/mobiteli?cp%5B0%5D=brand%3AApple&items_per_page=36",
    ]

    def parse(self, response):
        if "nabava.net" in response.url:
            products = response.css(".product")

            for product in products:
                item = WebscraperItem()
                name = product.css(".product-title::text").get()
                price = product.css(".product__price::text").get()
                link = product.css("a::attr(href)").get()

                item["id"] = str(uuid.uuid4())
                item["category"] = "iPhone"
                item["name"] = name.strip() if name else None
                item["price"] = price.replace("od", "").strip() if price else None
                item["link"] = f"https://www.nabava.net{link.strip()}" if link else None

                yield item

            next_page = response.css("a.next-page::attr(href)").get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)

        elif "svijet-medija.hr" in response.url:
            products = response.css("article.node--type-product")

            for product in products:
                item = WebscraperItem()
                name = product.css("span.field--name-title::text").get()
                price = (
                    product.css("span.product--teaser__content-price::text").get()
                    or product.css("span.product__pricing-discount::text").get()
                )
                link = product.css("h2 a::attr(href)").get()

                item["id"] = str(uuid.uuid4())
                item["category"] = "iPhone"
                item["name"] = name.strip() if name else None
                item["price"] = price.strip() if price else None
                item["link"] = response.urljoin(link.strip()) if link else None

                yield item

            next_page = response.css('a[rel="next"]::attr(href)').get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)
