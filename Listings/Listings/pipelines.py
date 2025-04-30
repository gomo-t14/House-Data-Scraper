# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class ListingsPipeline:
    def process_item(self, item, spider):
        return item
    
class PropcoPipeline:
    def process_item(self, item, spider):
        #Listing_ref cleaning
        if 'Listing_ref' in item:
            item['Listing_ref'] = self.remove_listing_ref(item['Listing_ref'])

            # Clean the 'Company' field
        if 'Company' in item:
            item['Company'] = self.remove_before_second_slash(item['Company'])

        # Clean the 'Price' field
        if 'Price' in item:
            item['Price'] = self.clean_price(item['Price'])

        # Clean the 'Area' fields
        if 'land_area' in item :
            item['land_area'] = self.clean_area(item['land_area'])

        if 'building_area' in item :
            item['building_area'] = self.clean_area(item['building_area'])



        return item
    





    #custom methods for the pipeline
    
    def remove_listing_ref(self, text):
        # Remove the pattern and return cleaned text
        cleaned_text = text.replace("Listing ref:", "")
        
        # Optionally strip any leading/trailing spaces after removal
        return cleaned_text.strip()
    

    def remove_before_second_slash(self, text):
        """Remove all text before and including the second '/' in the 'Company' URL."""
        # Find the position of the second '/'
        second_slash_pos = text.find('/', text.find('/') + 1)
        if second_slash_pos != -1:
            # Return the substring after the second '/'
            return text[second_slash_pos + 1:]
        return text.capitalize()  # Return the original text if no second '/' is found and capitalized
    
    def clean_price(self,price: str) -> str:
        # Remove 'USD', commas, and any leading/trailing whitespace
        cleaned_price = re.sub(r'USD|,|\s+', '', price).strip()
        return cleaned_price

    def clean_area(self,area: str) -> str:
    # Remove 'm²' and any surrounding whitespace
        cleaned_area = re.sub(r'\s*m²\s*', '', area)
        # Remove all commas
        cleaned_area = cleaned_area.replace(",", "")

        return cleaned_area.strip()


