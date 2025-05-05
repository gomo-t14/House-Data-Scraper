# Zimbabwe Real Estate Scraper 🏠

A web scraping project built using [Scrapy](https://scrapy.org/) to extract structured property listings from two major Zimbabwean real estate websites:

- [property.co.zw](https://www.property.co.zw/)
- [propertybook.co.zw](https://www.propertybook.co.zw/)

---

## 📌 Project Overview

This project scrapes detailed property listings, including metadata such as:

- Location (Suburb, City, Province)
- Agent and company information
- Pricing history (from 2015 to 2025)
- Property details (bedrooms, bathrooms, building and land area)
- Description and amenities
- Listing references and URLs

The scraper is structured to support both sources via separate spiders and item models.

---

## 📁 Repository Structure

real-estate-scraper/
├── scrapy.cfg
├── real_estate/
│ ├── init.py
│ ├── items.py # Scraped data models
│ ├── middlewares.py
│ ├── pipelines.py
│ ├── settings.py # Crawler settings
│ ├── spiders/
│ │ ├── init.py
│ │ ├── propertycozw_spider.py # Spider for property.co.zw
│ │ ├── propertybook_spider.py # Spider for propertybook.co.zw

# ✅ Sample Output
{
  "Property_type": "House",
  "Surbub": "Madokero",
  "City": "Harare West",
  "Province": "Harare",
  "bedrooms": "4",
  "bathrooms": "3",
  "Description": "This lovely property in Madokero...",
  "Listing_ref": "ALX218151",
  "amenities": ["Borehole", "Fitted Kitchen", "Garage"],
  "Price_2015": 115000.0,
  "Price_2025": "135000",
  "Company": "Alexcourt",
  "Agent": "Cris Kusikwenyu",
  "building_area": "250",
  "land_area": "450",
  "listing_url": "https://www.property.co.zw//for-sale/houses-alx218151"
}
