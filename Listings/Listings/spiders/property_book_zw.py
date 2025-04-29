import scrapy
from  Listings.items import Propbook_info 
from urllib.parse import urlparse


#define spider
class Prop_book(scrapy.Spider):
    name = "prop_book"

    start_urls = [ 
        "https://www.propertybook.co.zw/houses/for-sale",
        "https://www.propertybook.co.zw/flats_apartments/for-sale",
        "https://www.propertybook.co.zw/townhouses_complexes_clusters/for-sale",
        "https://www.propertybook.co.zw/cottages_garden-flats/for-sale",


    ]

    def parse(self, response):
        url = response.url #current page url
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')    #access parts of the url
        prop_category = path_parts[0] #type of property


        #find the listing cards
        #cards = response.xpath("//div[@class =  'propertyListings']//div[@class ='listingDetails']")
        cards = response.xpath("//div[contains(@class, 'listing')][@id]")

        next_page_url = response.xpath("//a[@class= 'page-link'][@rel = 'next']/@href").get() #url for next page 


        for card in cards:
            follow_url = card.xpath(".//a/@href").get() or "NULL" # url to more details
            location_details = card.xpath("normalize-space(.//div[@class= 'locationDetail']/text())").get() or "NULL" #location info


            #method meta store scraped data for next response
            page1_data = {
                "Listing_url":follow_url,
                "Location_info": location_details,
                "Property_type": prop_category,

            }
            #follow for more details
            if follow_url:
                yield scrapy.Request(url= follow_url,
                                     callback = self.listing_detail,
                                     meta = {"page1_data":page1_data})
        #pagination
        yield scrapy.Request(url = next_page_url , callback = self.parse)



    def listing_detail(self, response):
        item = Propbook_info() #instantiate item object
        #instantiate meta
        page1_data = response.meta['page1_data']

        #get details from section 1
        prop_section1 = response.xpath("//div[@class ='property-title']")#containes price, listing ref 
        item['Price'] = prop_section1.xpath("normalize-space(.//h4/text())").get() or "NULL" #listing price
        item['listing_ref'] = prop_section1.xpath("normalize-space(.//span/text())").get() or "NULL" # REF ID


        item['Real_estate_company'] = response.xpath("//div[@class = 'block']//div//h5/text()").get() or "NULL" #company name


        #get details from section 2
        prop_section2 = response.xpath("//div[@class = 'property-info']")
        item['Listing_date'] =  prop_section2.xpath("normalize-space(.//div[@class = 'listed-date']/text())").get() or "NULL" #date listing was published

       
        item['bedrooms'] = response.xpath("normalize-space(//div[@class='property-info']//ul//li[i[contains(@class, 'fa-bed')]]/text()[normalize-space()])").get() or "NULL" #bedrooms        
        item['bathrooms'] = response.xpath("normalize-space(//div[@class='property-info']//ul//li[i[contains(@class, 'fa-bath')]]/text()[normalize-space()])").get() or "NULL" #number of bathrooms
        item['lounges'] = response.xpath("normalize-space(//div[@class='property-info']//ul//li[i[contains(@class, 'fa-couch')]]/text()[normalize-space()])").get() or "NULL"#number of lounges
        item['prop_area'] = response.xpath("normalize-space(//div[@class='property-info']//ul//li[span[contains(@class, 'property-size')]]/text()[normalize-space()])").get() or "NULL"#property size 

        #property description
        item['prop_description'] =  response.xpath("//div[@class='propertyDescription']//text()[normalize-space()]").getall() or "NULL" 

        #Amenities
        
        #get prop features section
        amenities = response.xpath("//div[@class='row property-features']//div[@class='col-12 feature']")

        amenities_dict = {} #dictionary to hold amaneites key value pairs

        for m in amenities:
            span_class = m.xpath(".//span[1]/@class").get()
            #value = m.xpath(".//span[1]/text()").get()
            #amenity = m.xpath(".//span[2]/text()").get()

            #check if the class have a value or tick
            if span_class == 'value':
                value = m.xpath(".//span[1]/text()").get()or "NULL"  #assign the value to value attribute 

            else:
                value = "1" #since it is only a check mark it signifies that only one instance of this amenity is available

            amenity = m.xpath(".//span[2]/text()").get()or "NULL"

            if amenity:
                amenities_dict[amenity] = value


        #amenities dict item
        item['amenities'] = amenities_dict

        #set the data into descriptive variables
        temp_location =  page1_data.get("Location_info").split(",")

        item['Surbub'] = temp_location[0].strip() if len(temp_location) > 0 else "NULL"
        item['City'] = temp_location[1].strip() if len(temp_location) > 0 else "NULL"
        item['Province'] = temp_location[2].strip() if len(temp_location) > 0 else "NULL"

        #listing url 
        item['listing_url'] = page1_data.get('Listing_url')or "NULL"

        #Property type 
        item['Property_type'] = page1_data.get('Property_type')or "NULL"




        '''
        combined_data = {
            #**page1_data,
            #"Price":Price,
            #"Listing ref": listing_ref,
            #"Company": Real_estate_company,
            #"Date":Listing_date,
            #"bedrooms": bedrooms,
            #"bathrooms": bathrooms,
            #"Lounges": lounges,
            #"Property-area":prop_area,
            #"Property Description": prop_description,
            "amenities": amenities_dict,

        }
        '''
        yield item