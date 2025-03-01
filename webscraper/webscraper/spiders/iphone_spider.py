import uuid
import scrapy

class IphoneSpider(scrapy.Spider): 
    name = "iphone_spider"
    allowed_domains = ["nabava.net"]
    start_urls= [
        "https://www.nabava.net/mobiteli?se=1&cod=&cdo="
    ]
    

    def parse(self, response):

        products = response.css(".product")

        for product in products: 

            name = product.css(".product-title::text").get() 
            price = product.css(".product__price::text").get()
            link = product.css('a').attrib['href']


            yield{
                "id" : str(uuid.uuid4()),
                "category" : "Iphone",
                "name" : name.strip() if name else None,
                "price" : price.strip() if price else None,
                "link" : "https://www.nabava.net" + link.strip() if link else None,

            }
        next_page = response.css("a.next-page::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

            