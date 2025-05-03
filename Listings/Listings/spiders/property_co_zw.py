import scrapy
from Listings.items import PropertyListing
import json


class ListingsSpider(scrapy.Spider):
    name = "prop_co_zw"#spider name

    start_urls =["https://www.property.co.zw/houses-for-sale",] #scraping urls

    #spider pipeline
    custom_settings = {
        'ITEM_PIPELINES': {
            'Listings.pipelines.PropcoPipeline': 1,
        },
    }


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

        #Property type 
        item['Property_type'] = "House"

        #here we extract details relating to the listings location
        location_details = response.xpath("//h1[@id='ListingTitle']/following-sibling::div/text()").get()

        #set the data into descriptive variables
        temp_location =  location_details.split(",")

        item['Surbub'] = temp_location[0].strip() or None 
        item['City'] = temp_location[1].strip() or None 
        item['Province'] = temp_location[2].strip() or None 

        #Listing Specifications
        
        item['bedrooms'] = response.xpath("normalize-space(//div[@class='bed']/text()[normalize-space()])").get() or None 
        item['bathrooms']  = response.xpath("normalize-space(//div[@class='bath']//text()[normalize-space()])").get() or None 


        #Listing Description
        Description_extract = response.xpath("//h2[normalize-space(text())='Description']/following-sibling::div[br]//text()").getall() or None 
        item['Description'] = ' '.join([text.strip() for text in Description_extract if text.strip()]) 


        #Amenities
        amenities = response.xpath("//h2[normalize-space(text()='Amenities')]/following-sibling::div/div")


        #Listing ref
        item['Listing_ref'] = response.xpath("//span[contains(text(), 'Listing ref')]/text()").get() or None 
        amenities_list = [m.xpath("./div[2]/text()").get() for m in amenities]
        item['amenities'] = [a for a in amenities_list if a] 

        #lets get the labels and values list
        data_str = response.xpath('//canvas/@data-chart-data').get()or None  # returns json object of price and labels
        data = json.loads(data_str) #parse json object 
        values = data["Values"] #list of price values
        labels = data["Labels"] #list of year labels

        #add values to item model
        for label, value in zip(labels, values):
            item[f'Price_{label}'] = value




        #Adding page1 data to item model
        item['Company'] = page1_data.get('Company')
        item['Agent'] = page1_data.get('Agent')
        item['Price_2025'] = page1_data.get('Price')
        item['building_area'] = page1_data.get('building area')
        item['land_area'] = page1_data.get('land size')
        item['listing_url'] = page1_data.get('Listing_url')


        yield item
      

        



        