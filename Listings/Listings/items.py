# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ListingsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PropertyListing(scrapy.Item):
    Listing_ref = scrapy.Field()
    listing_url = scrapy.Field()
    Property_type = scrapy.Field(default = 'House')
    Company = scrapy.Field()
    Agent = scrapy.Field()
    Price_2025 = scrapy.Field()

    Surbub = scrapy.Field()
    City = scrapy.Field()
    Province = scrapy.Field()

    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    building_area = scrapy.Field()
    land_area = scrapy.Field()

    Description = scrapy.Field()
    amenities = scrapy.Field()

    Price_2015 = scrapy.Field()
    Price_2016 = scrapy.Field()
    Price_2017 = scrapy.Field()
    Price_2018 = scrapy.Field()
    Price_2019 = scrapy.Field()
    Price_2020 = scrapy.Field()
    Price_2021 = scrapy.Field()
    Price_2022 = scrapy.Field()
    Price_2023 = scrapy.Field()
    Price_2024 = scrapy.Field()


##item for propertybook zw 
class Propbook_info(scrapy.Item):
    listing_ref = scrapy.Field()
    listing_url = scrapy.Field()
    Real_estate_company = scrapy.Field()
    Property_type = scrapy.Field()
    Price = scrapy.Field()
    Surbub = scrapy.Field()
    City = scrapy.Field()
    Province = scrapy.Field()
    Listing_date =scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    lounges = scrapy.Field()
    prop_area = scrapy.Field()
    prop_description = scrapy.Field()
    amenities = scrapy.Field()
