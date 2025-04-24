import scrapy

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
            
            #follow url
            detail_url = card.xpath(".//a[starts-with(normalize-space(text()), 'USD ')]/@href").get()

           

            page1_data = {
                "Company": Real_estate_company,
                "Agent": Real_estate_agent,
                "Price": Price,
            }

            if detail_url:
                yield scrapy.Request(url = f"https://www.property.co.zw/{detail_url}",
                                     callback=self.listing_details,
                                     meta={"page1_data": page1_data})
        #pagination
        yield scrapy.Request(url = next_page_url , callback = self.parse)
        #print("next page")

    def listing_details(self,response):
        #data from page1 
        page1_data = response.meta['page1_data']

        #here we extract details relating to the listings location
        location_details = response.xpath("//h1[@id='ListingTitle']/following-sibling::div/text()").get()

        #set the data into descriptive variables
        temp_location =  location_details.split(",")
        Surbub = temp_location[0]
        City = temp_location[1]
        Province = temp_location[2]

        #Listing Specifications
        #bedrooms = response.xpath("//div[@class='bed']//text()").get() #number of bedrooms
        bedrooms = response.xpath("normalize-space(//div[@class='bed']/text()[normalize-space()])").get()
        bathrooms = response.xpath("normalize-space(//div[@class='bath']//text()[normalize-space()])").get() #number of bathrooms
        building_area = response.xpath("normalize-space(//div[@class='area'][svg]//text()[normalize-space()])").get() #area covered by building
        land_area = response.xpath("normalize-space(//div[@class='area'][img]//text()[normalize-space()])").get() #total are of plot of land

        #Listing Description
        Description_extract = response.xpath("//h2[normalize-space(text())='Description']/following-sibling::div[br]//text()").getall()
        Description = ' '.join([text.strip() for text in Description_extract if text.strip()])


        #Amenities
        amenities = response.xpath("//h2[normalize-space(text()='Amenities')]/following-sibling::div/div")
        amenities_list = []
        for m in amenities:
            amenity = m.xpath("./div[2]/text()").get()
            amenities_list.append(amenity)


        #Listing ref
        Listing_ref = response.xpath("//span[contains(text(), 'Listing ref')]/text()").get()


        

        #meta for location data 
        yield  {
            "Listing_ref": Listing_ref,
            **page1_data,
            "Surbub": Surbub,
            "City": City,
            "Province":Province,
            "bedrooms": bedrooms,
            "bathrooms":bathrooms,
            "building_area":building_area,
            "land_area":land_area,
            "Description":Description,
            "amenities":amenities_list,
            "next_page":next_page_url,
        }

      

        



        