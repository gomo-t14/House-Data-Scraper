import scrapy


#define spider
class Prop_book(scrapy.Spider):
    name = "prop_book"

    start_urls = [ "https://www.propertybook.co.zw/houses/for-sale",

    ]

    def parse(self, response):
        #find the listing cards
        #cards = response.xpath("//div[@class =  'propertyListings']//div[@class ='listingDetails']")
        cards = response.xpath("//div[@class]//div[@id]")

        for card in cards:
            follow_url = card.xpath(".//a/@href").get() or "NULL" # url to more details
            location_details = card.xpath("normalize-space(.//div[@class= 'locationDetail']/text())").get() or "NULL" #location info


            #method meta store scraped data for next response
            page1_data = {
                "Listing_url":follow_url,
                "Location_info": location_details,

            }
            if follow_url:
                yield scrapy.Request(url= follow_url,
                                     callback = self.listing_detail,
                                     meta = {"page1_data":page1_data})


    def listing_detail(self, response):
        #instantiate meta
        page1_data = response.meta['page1_data']

    
        prop_section1 = response.xpath("//div[@class ='property-title']")#containes price, listing ref 

        for prop in prop_section1:
            Price = prop.xpath(".//h4/text()").get or "NULL" #listing price
            listing_ref = prop.xpath(".//span/text()").get or "NULL" # REF ID