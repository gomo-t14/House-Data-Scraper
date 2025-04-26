import scrapy
from Listings.items import PropertyListing


class ListingsSpider(scrapy.Spider):
    name = "prop_co_zw"

    start_urls =["https://www.property.co.zw/houses-for-sale",]

    def parse(self, response):
        #get listing cards
        cards = response.xpath(".//div[@class='result-cards']/div[@id]")

        #next page url
        next_page_url = response.xpath("//a[@class = ' next']/@href").get()

        for card in cards:
            Real_estate_company = card.xpath("./div/div/a[1]/@href").get()
            Real_estate_agent = card.xpath("./div/div/a[2]/text()").get()
            Price = card.xpath(".//a[starts-with(normalize-space(text()), 'USD ')]/text()").get()
            building_area = card.xpath("normalize-space(.//span[contains(@class, 'building-area')]/text()[normalize-space()])").get()
            land_size = card.xpath("normalize-space(.//span[contains(@class, 'land-size')]/text()[normalize-space()])").get()

            
            #follow url
            detail_url = card.xpath(".//a[starts-with(normalize-space(text()), 'USD ')]/@href").get()

            #full request url for followed  listings
            follow_url = f"https://www.property.co.zw/{detail_url}"

           

            page1_data = {
                "Company": Real_estate_company,
                "Agent": Real_estate_agent,
                "Price": Price,
                "building area":building_area,
                "land size": land_size,
                "Listing_url": follow_url,
            }

            if detail_url:
                #follow request
                yield scrapy.Request(url = follow_url,
                                     callback=self.listing_details,
                                     meta={"page1_data": page1_data})
                
        #pagination
        yield scrapy.Request(url = next_page_url , callback = self.parse)


    def listing_details(self,response):
        #data from page1 
        page1_data = response.meta['page1_data']

        ##instantiate item object
        item = PropertyListing()

        #here we extract details relating to the listings location
        location_details = response.xpath("//h1[@id='ListingTitle']/following-sibling::div/text()").get()

        #set the data into descriptive variables
        temp_location =  location_details.split(",")

        item['Surbub'] = temp_location[0].strip() if len(temp_location) > 0 else "NULL"
        item['City'] = temp_location[1].strip() if len(temp_location) > 0 else "NULL"
        item['Province'] = temp_location[2].strip() if len(temp_location) > 0 else "NULL"

        #Listing Specifications
        
        item['bedrooms'] = response.xpath("normalize-space(//div[@class='bed']/text()[normalize-space()])").get() or "NULL"
        item['bathrooms']  = response.xpath("normalize-space(//div[@class='bath']//text()[normalize-space()])").get() or "NULL" #number of bathrooms


        #Listing Description
        Description_extract = response.xpath("//h2[normalize-space(text())='Description']/following-sibling::div[br]//text()").getall()
        item['Description'] = ' '.join([text.strip() for text in Description_extract if text.strip()]) or "NULL"


        #Amenities
        amenities = response.xpath("//h2[normalize-space(text()='Amenities')]/following-sibling::div/div")


        #Listing ref
        item['Listing_ref'] = response.xpath("//span[contains(text(), 'Listing ref')]/text()").get() or "NULL"
        amenities_list = [m.xpath("./div[2]/text()").get() for m in amenities]
        item['amenities'] = [a for a in amenities_list if a] or ['NULL']

        #Adding page1 data to item model
        item['Company'] = page1_data.get('Company', 'NULL')
        item['Agent'] = page1_data.get('Agent', 'NULL')
        item['Price'] = page1_data.get('Price', 'NULL')
        item['building_area'] = page1_data.get('building area', 'NULL')
        item['land_area'] = page1_data.get('land size', 'NULL')
        item['listing_url'] = page1_data.get('Listing_url', 'NULL')


        yield item
      

        



        