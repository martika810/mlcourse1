from productscraper import ProductScraper
from bs4 import BeautifulSoup
import time
import pandas as pd

class PageScraper:
    def __init__(self, browser):
        self.browser = browser

    def isProductUrl(self, url):
        return url.find('/store/product/')>-1

    def count_products_in_page(self, html,url):
        if not self.isProductUrl(url):
            html_soup_parser = BeautifulSoup(html, 'html.parser')
            all_products_loaded_in_beatifulsoup = html_soup_parser.find_all('a', class_='pic-rind')
            return len(all_products_loaded_in_beatifulsoup)
        else:
            return 0

    def extract_allproduct_in_this_page(self, browser, filename_to_save, number_product, dataframe):

        for product_index in range(1,number_product+1):
            all_product_pages = browser.find_elements_by_css_selector('a.pic-rind')

            all_product_pages[product_index-1].click()
            time.sleep(3)
            product_scraper = ProductScraper(browser)
            product_serie = product_scraper.extract_product()
            dataframe = dataframe.append(product_serie,ignore_index=True)

        dataframe.to_csv(filename_to_save)
        return dataframe

