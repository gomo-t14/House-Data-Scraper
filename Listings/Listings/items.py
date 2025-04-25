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
    Company = scrapy.Field()
    Agent = scrapy.Field()
    Price = scrapy.Field()

    Surbub = scrapy.Field()
    City = scrapy.Field()
    Province = scrapy.Field()

    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    building_area = scrapy.Field()
    land_area = scrapy.Field()

    Description = scrapy.Field()
    amenities = scrapy.Field()