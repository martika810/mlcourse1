from pagescraper import PageScraper
import pandas as pd
from pathlib import Path
import time

class CategoryScraper:
    def __init__(self, browser):
        self.browser = browser

    def crawling_to_findall_pages(self, initial_url,filename_to_save):

        page_scraper = PageScraper(self.browser)

        try:

            self.browser.get(initial_url)
            if(page_scraper.isProductUrl(self.browser.current_url)):
                self.browser.refresh()
                self.browser.back()

            next_button = self.browser.find_element_by_css_selector('div.ui-pagination-navi.util-left .ui-pagination-next')
            isLastPage = next_button.get_attribute('class').find('disabled')>-1

            dataframe_file = Path(filename_to_save)
            if(not dataframe_file.exists()):
                dataframe = pd.DataFrame()
            else:
                dataframe = pd.read_csv(filename_to_save)

            if(isLastPage):
                number_product_in_this_page = page_scraper.count_products_in_page(self.browser.page_source, self.browser.current_url)
                print('allproducts loaded by beautiful: {}'.format(number_product_in_this_page))
                page_scraper.extract_allproduct_in_this_page(self.browser,filename_to_save,number_product_in_this_page,dataframe)
                return True


            while not isLastPage:
                number_product_in_this_page = page_scraper.count_products_in_page(self.browser.page_source, self.browser.current_url)
                print('allproducts loaded by beautiful: {}'.format(number_product_in_this_page))
                dataframe = page_scraper.extract_allproduct_in_this_page(self.browser,filename_to_save,number_product_in_this_page,dataframe)

                next_button = self.browser.find_element_by_css_selector('div.ui-pagination-navi.util-left a.ui-pagination-next')
                next_button.click()
                time.sleep(2)
                next_button = self.browser.find_element_by_css_selector('div.ui-pagination-navi.util-left a.ui-pagination-next')
                isLastPage = next_button.get_attribute('class').find('disabled')>-1



            # Scan last page
            number_product_in_this_page = page_scraper.count_products_in_page(self.browser.page_source, self.browser.current_url)
            print('allproducts loaded by beautiful: {}'.format(number_product_in_this_page))
            page_scraper.extract_allproduct_in_this_page(self.browser, filename_to_save, number_product_in_this_page, dataframe)

            return True

        except Exception as e:
            return False

    def scrape(self, initial_url,filename_to_save):
        got_to_end = False
        while not got_to_end:

            got_to_end = self.crawling_to_findall_pages(initial_url,filename_to_save)
            initial_url = self.browser.current_url

