import scrapy

class ListingsSpider(scrapy.Spider):
    name = "prop_co_zw"

    start_urls =["https://www.property.co.zw/houses-for-sale",]

    def parse(self, response):
        #get listing cards
        cards = response.xpath(".//div[@class='result-cards']/div[@id]")

        for card in cards:
            Real_estate_company = card.xpath("./div/div/a[1]/@href").get()
            Real_estate_agent = card.xpath("./div/div/a[2]/text()").get()
            Price = card.xpath(".//a[starts-with(normalize-space(text()), 'USD ')]/text()").get()
            
            #follow url
            detail_url = card.xpath(".//a[starts-with(normalize-space(text()), 'USD ')]/@href").get()

            yield {
                "Company": Real_estate_company,
                "Agent": Real_estate_agent,
                "Price": Price,
            }

        