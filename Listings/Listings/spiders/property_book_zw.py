import scrapy


#define spider
class Prop_book(scrapy.Spider):
    name = "prop_book"

    start_urls = [ "https://www.propertybook.co.zw/houses/for-sale",

    ]

    def parse(self, response):
        #find the listing cards
        #cards = response.xpath("//div[@class =  'propertyListings']//div[@class ='listingDetails']")
        cards = response.xpath("//div[contains(@class, 'listing')][@id]")

        for card in cards:
            follow_url = card.xpath(".//a/@href").get() or "NULL" # url to more details
            location_details = card.xpath("normalize-space(.//div[@class= 'locationDetail']/text())").get() or "NULL" #location info


            #method meta store scraped data for next response
            page1_data = {
                "Listing_url":follow_url,
                "Location_info": location_details,

            }
            #follow for more details
            if follow_url:
                yield scrapy.Request(url= follow_url,
                                     callback = self.listing_detail,
                                     meta = {"page1_data":page1_data})


    def listing_detail(self, response):
        #instantiate meta
        page1_data = response.meta['page1_data']

        #get details from section 1
        prop_section1 = response.xpath("//div[@class ='property-title']")#containes price, listing ref 
        Price = prop_section1.xpath("normalize-space(.//h4/text())").get() or "NULL" #listing price
        listing_ref = prop_section1.xpath("normalize-space(.//span/text())").get() or "NULL" # REF ID


        Real_estate_company = response.xpath("//div[@class = 'block']//div//h5/text()").get() or "NULL" #company name


        #get details from section 2
        prop_section2 = response.xpath("//div[@class = 'property-info']")
        Listing_date =  prop_section2.xpath("normalize-space(.//div[@class = 'listed-date']/text())").get() or "NULL" #date listing was published

       
        bedrooms = response.xpath("normalize-space(//div[@class='property-info']//ul//li[i[contains(@class, 'fa-bed')]]/text()[normalize-space()])").get() or "NULL" #bedrooms        
        bathrooms = response.xpath("normalize-space(//div[@class='property-info']//ul//li[i[contains(@class, 'fa-bath')]]/text()[normalize-space()])").get() or "NULL" #number of bathrooms
        lounges = response.xpath("normalize-space(//div[@class='property-info']//ul//li[i[contains(@class, 'fa-couch')]]/text()[normalize-space()])").get() or "NULL"#number of lounges
        prop_area = response.xpath("normalize-space(//div[@class='property-info']//ul//li[span[contains(@class, 'property-size')]]/text()[normalize-space()])").get() or "NULL"#property size 
        
        combined_data = {
            **page1_data,
            "Price":Price,
            "Listing ref": listing_ref,
            "Company": Real_estate_company,
            "Date":Listing_date,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "Lounges": lounges,
            "Property-area":prop_area,
        }
        
        yield combined_data