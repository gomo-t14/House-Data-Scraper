# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class ListingsPipeline:
     #custom methods for the pipeline
    
    def remove_listing_ref(self, text):
        # Remove the pattern and return cleaned text
        cleaned_text = text.replace("Listing ref:", "")
        
        # Optionally strip any leading/trailing spaces after removal
        return cleaned_text.strip()
    
    '''
    def remove_before_second_slash(self, text):
        """Remove all text before and including the second '/' in the 'Company' URL."""
        # Find the position of the second '/'
        second_slash_pos = text.find('/', text.find('/') + 1)
        if second_slash_pos != -1:
            # Return the substring after the second '/'
            return text[second_slash_pos + 1:]
        return text.capitalize()  # Return the original text if no second '/' is found and capitalized
    '''
    def remove_before_second_slash(self, text):
        text.replace('/estate-agents/','')
        text.capitalize()

        return text
    
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
    
    def replace_text(self , key, replace_string) :
        key = key.replace(replace_string,"")

        return key
    


    #clean area
    def area_converter(self, area):
        # Normalize input (remove spaces and lowercase for easy matching)
        raw_area = area.strip().replace(" ", "").lower()

        # Determine unit from string
        if "ha" in raw_area:
            unit = "Ha"
        elif "ac" in raw_area:
            unit = "Ac"
        else:
            unit = "m²"  # assume it's already in square meters

        # Clean numeric part: remove commas, units, and symbols
        cleaned_area = re.sub(r"[,m]", "", raw_area)
        cleaned_area = re.sub(r"(ha|ac)", "", cleaned_area, flags=re.IGNORECASE)
        cleaned_area = cleaned_area.strip()

        # Convert
        try:
            value = float(cleaned_area)
        except ValueError:
            raise ValueError(f"Could not parse area: {area}")

        if unit == "Ha":
            return value * 10000
        elif unit == "Ac":
            return value * 4046.8564224
        else:
            return value  # already in m²
        
    def clean_prop_description(self, description_list):
    #remove new lines and strip excess whitespace
        cleaned = [desc.replace('\n', '').strip() for desc in description_list]
        return cleaned


    
class PropcoPipeline(ListingsPipeline):
    def process_item(self, item, spider):
        #Listing_ref cleaning
        if 'Listing_ref' in item:
            item['Listing_ref'] = self.remove_listing_ref(item['Listing_ref'])

        #Clean the 'Company' field
        #if 'Company' in item:
        #   item['Company'] = self.remove_before_second_slash(item['Company'])

        # Clean the 'Price' field
        if 'Price' in item:
            item['Price'] = self.clean_price(item['Price'])

        # Clean the 'Area' fields
        if 'land_area' in item :
            item['land_area'] = self.clean_area(item['land_area'])

        if 'building_area' in item :
            item['building_area'] = self.clean_area(item['building_area'])



        return item
    

class PropbookPipeline(ListingsPipeline):
    def process_item(self, item, spider):

        # Clean the 'Price' field
        if 'Price' in item:
            item['Price'] = self.clean_price(item['Price'])

        #Clean listing date 
        if 'Listing_date' in item:
            item['Listing_date'] = self.replace_text(item['Listing_date'],"Last Updated: ")

    
        #Clean bedrooms
        if 'bedrooms' in item:
            item['bedrooms'] = self.replace_text(item['bedrooms']," Beds")

        #Clean bathrooms
        if 'bathrooms' in item:
            item['bathrooms'] = self.replace_text(item['bathrooms']," Baths")
            item['bathrooms'] = self.replace_text(item['bathrooms']," Bath") # edge case

        #Clean lounges
        if 'lounges' in item:
            item['lounges'] = self.replace_text(item['lounges']," Lounge")
            item['lounges'] = self.replace_text(item['lounges']," Lounges")#edge case 

        #are_converter
        if 'prop_area' in item:
            item['prop_area'] = self.area_converter(item['prop_area'])

        #prop_description
        if 'prop_description' in item:
            item['prop_description'] = self.clean_prop_description(item['prop_description'])

        
        return item



       
    
    
    
    
    






   