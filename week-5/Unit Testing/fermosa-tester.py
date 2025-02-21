import unittest
from unittest.mock import Mock, patch, MagicMock
from bs4 import BeautifulSoup
from fermoa2xl import Sansevierias



class TestSansevierias(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://fermosaplants.com/collections/sansevieria?page="
        self.scraper = Sansevierias(self.base_url)
        
        self.sample_listings_html = '''
            <div class="product-item-v5">
                <h4 class="title-product">
                    <a href="/collections/sansevieria/products/sansevieria-ghost">Sansevieria Trifasciata 'Ghost'</a>
                </h4>
                <span class="price">Rs. 859.00</span>
            </div>
            <div class="product-item-v5">
                <h4 class="title-product">
                    <a href="/collections/sansevieria/products/sansevieria-hybrid-tower">Sansevieria Hybrid 'Tower'</a>
                </h4>
                <span class="price">Rs. 750.00</span>
            </div>
            <div class="product-item-v5">
                <h4 class="title-product">
                    <a href="/collections/sansevieria/products/sansevieria-gracilis-clump">Sansevieria Gracilis Clump</a>
                </h4>
                <span class="price">Rs. 850.00</span>
            </div>
        '''
        
        self.sample_product_page_html = [
            '''<div class="pd_summary">
                About Sansevieria Trifasciata - Beautiful Snake Plant
            </div>
            <div class="desc product-desc">
                1. Trifasciata
                2. Laurentii
                3. Black Gold
            </div>''',
            '''
            <div class="pd_summary">
                Scientific Name- Sansevieria  About Combo
            </div>
            <div class="desc product-desc">
                Scientific Name- Sansevieria 
                About Combo Offer (L) - ﻿1. Coppertone, 2. Silver Siam, 
                3. Silver Princess, 5. Fernwood
                Comes bare root.
                Images are for reference purposes only. 
            </div>''',
            '''
            <div class="pd_summary">
                about Sansevieria Bella silver - avnjiascoil.....
            </div>
            <div class="desc product-desc">
                Comes bare root.
                Images are for reference purposes only. 
            </div>''',
            '''
            <div class="pd_summary">
                Moonshine Mutant
            </div>
            <div class="desc product-desc">
                Moonshine Mutant
            </div>''']


    @patch('requests.get')
    def test_get_soup(self, mock_get):
        mock_res = Mock()
        mock_res.status_code = 200
        mock_res.content = "<html><body>Test</body></html>"
        mock_get.return_value = mock_res
        
        soup = self.scraper._get_soup("test_url")
        self.assertIsInstance(soup, BeautifulSoup)
        self.assertEqual(str(soup), "<html><body>Test</body></html>")
        
        mock_res.status_code = 404
        with self.assertRaises(ValueError):
            self.scraper._get_soup("test_url")

    @patch('fermoa2xl.Sansevierias._get_soup')
    def test_scrape_page(self,mock_get_soup):
        product_page_soup = BeautifulSoup(self.sample_product_page_html[0], 'html.parser')
        mock_get_soup.return_value = product_page_soup
        
        main_page_soup = BeautifulSoup(self.sample_listings_html, 'html.parser')
        
        data = self.scraper.scrape_page(main_page_soup)
        
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)
        
        first_entry = data[0]
        self.assertEqual(first_entry[0], "Sansevieria Trifasciata 'Ghost'")
        self.assertEqual(first_entry[1], "859.00")
        self.assertFalse(first_entry[2])
        self.assertEqual(first_entry[3], 1)
        self.assertNotIn("combo", first_entry[4]) 
        self.assertNotIn("plant", first_entry[4]) 
        self.assertTrue(first_entry[5].startswith("https://fermosaplants.com"))

        empty_page_soup = BeautifulSoup('', 'html.parser')
        with self.assertRaises(AssertionError):
            self.scraper.scrape_page(empty_page_soup)
        

    def test_extract_names(self):
        product_page_one_soup = BeautifulSoup(self.sample_product_page_html[0], 'html.parser')
        names_list = self.scraper.extract_names(product_page_one_soup,True)
        self.assertEqual(set(names_list), set(['Trifasciata', 'Laurentii', 'Black Gold']))

        product_page_two_soup = BeautifulSoup(self.sample_product_page_html[1], 'html.parser')
        names_list = self.scraper.extract_names(product_page_two_soup,True)
        self.assertEqual(set(names_list), set(['Fernwood', 'Silver Princess', 'Coppertone', 'Silver Siam']))
        
        product_page_three_soup = BeautifulSoup(self.sample_product_page_html[2], 'html.parser')
        names_list = self.scraper.extract_names(product_page_three_soup,False)
        self.assertEqual(set(names_list), set(['Bella silver']))

        product_page_four_soup = BeautifulSoup(self.sample_product_page_html[3], 'html.parser')
        names_list = self.scraper.extract_names(product_page_four_soup,False)
        self.assertEqual(names_list, [])

    @patch('fermoa2xl.Sansevierias._get_soup')
    @patch('fermoa2xl.Sansevierias.scrape_page')
    def test_scrape_from(self, mock_get_soup, mock_scrape_page):
        mock_get_soup.return_value = BeautifulSoup(self.sample_listings_html, 'html.parser')
        mock_scrape_page.side_effect = [
            list(["Product1", "999", False, 1, "plant", "url1", "Name1"]),
            AssertionError()
        ]
        
        self.scraper.scrape_from(1)
        
        self.assertEqual(mock_scrape_page.call_count, 2)
   

if __name__ == '__main__':
    unittest.main()