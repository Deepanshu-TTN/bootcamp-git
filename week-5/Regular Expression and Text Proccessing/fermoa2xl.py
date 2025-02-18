from bs4 import BeautifulSoup
from openpyxl import Workbook
import requests
import re


class Sansevierias:
    def __init__(self, base_url, ws):
        self.domain = "https://fermosaplants.com"
        self.base_url = base_url
        self.ws = ws
        self.patterns = {
            'is_Variegated': re.compile(r'variegated', re.IGNORECASE),
            'listing_combo_amount': re.compile(r'combo.*of\s([0-9]+)', re.IGNORECASE),
            'listing_type': re.compile(r'combo|clump|Leaf|plant|pub', re.IGNORECASE)
        }


    def scrape_page(self, page_url):
        res = requests.get(page_url)
        soup = BeautifulSoup(res.content, 'html.parser')
        sansevierias = soup.find_all("div", class_="product-item-v5")
        
        #raise error if no items are fetched
        assert len(sansevierias)>0

        #simple function that returns a true value or the object itself if object exists otherwise a false value
        get_or_default = lambda obj, true, false: true or obj if obj else false

        for lising in sansevierias:

            listing_name = lising.find('h4', class_='title-product')
            listing_price = lising.find('p', class_='price-product')

            listing_url_ref = listing_name.find('a')['href'] #only 1 level below listing_name object so use it as the parent
            listing_combo_amount_ref = self.patterns['listing_combo_amount'].search(listing_name.text) #broke to ref since have to get combo number from same object later

            listing_url = self.domain + listing_url_ref
            is_Variegated = get_or_default(self.patterns['is_Variegated'].search(listing_name.text), True, False) 
            listing_combo_amount = get_or_default(listing_combo_amount_ref, None, None)  
            listing_types = get_or_default(self.patterns['listing_type'].findall(listing_name.text), None, [])


            listing_data = [
                listing_name.text.strip(), 
                listing_price.text.strip(), 
                is_Variegated, '1' if not listing_combo_amount else listing_combo_amount.groups()[0], 
                ', '.join(set(types.lower() for types in listing_types)), 
                listing_url
                            ]
            self.ws.append(listing_data)
            # print(listing_data)

    def scrape_from(self, page_number):
        while True:
            try:
                curr_url = self.base_url+str(page_number)
                res_flag = requests.get(curr_url)
                print(page_number)
                print(res_flag.status_code)
                self.scrape_page(curr_url)
                page_number+=1
            except AssertionError:
                break


if __name__ == '__main__':
    #cant save the file twice
    wb = Workbook(write_only=True)

    #get the active sheet or none
    ws = wb.create_sheet("Sansevierias")

    #add headings
    ws.append(['Product Name', 'Price', 'Variegated', 'Combo Amount', 'Listing Types', 'Product Url'])

    base_url = "https://fermosaplants.com/collections/sansevieria?page="
    fermosa_scraper = Sansevierias(base_url, ws)

    fermosa_scraper.scrape_from(page_number=1)

    wb.save('plantbook.xlsx')
