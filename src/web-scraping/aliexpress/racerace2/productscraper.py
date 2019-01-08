from bs4 import BeautifulSoup
import pandas as pd

class ProductScraper:
    def __init__(self, browser):
        self.browser = browser

    def extract_product_price(self, html_parser):

        currency = html_parser.select('#j-product-detail-bd > div.store-detail-main div.product-price > div > div.p-price-detail.util-clearfix > div > div > span.p-symbol')[0].text

        prices = html_parser.select('#j-sku-discount-price > span')
        isDiscountedPrice = len(prices)>0
        if isDiscountedPrice:
            if(len(prices)>1):
                first_price = prices[0].text
                second_price = prices[1].text
                product_price= currency+''+first_price+'-'+second_price
            else:
                first_price = html_parser.select('#j-sku-discount-price')[0].text
                product_price = currency+' '+first_price
        else:
            prices = html_parser.select('#j-sku-price > span')
            if(len(prices)>1):
                first_price = prices[0].text
                second_price = prices[1].text
                product_price= currency+''+first_price+'-'+second_price
            else:
                first_price = html_parser.select('#j-sku-price')[0].text
                product_price = currency+' '+first_price

        return product_price

    def extract_product_data(self, product_html_page):
        product_dict = {}
        html_parser = BeautifulSoup(product_html_page, 'html.parser')
        images = html_parser.select('#j-image-thumb-list > li > span > img')
        images_values = ''
        for image in images:
            images_values = images_values + ';' + image.get_attribute_list('src')[0]

        product_dict['images'] = images_values[1:]
        title = html_parser.select('#j-product-detail-bd div.store-detail-main div h1.product-name')[0].text
        product_dict['title'] = title

        product_dict['price'] = self.extract_product_price(html_parser)

        #attributes
        attributes = html_parser.select('#j-product-info-sku > dl.p-property-item')

        for attribute in attributes:
            title = attribute.select('dt.p-item-title')[0].text[:-1]
            values_list =attribute.select('dd.p-item-main li span')
            values = ''
            for attribute_value in values_list:
                values = values + ';' + attribute_value.text
            product_dict[title] = values[1:]

        #specifications
        specification_list = html_parser.select('#j-product-desc div.ui-box-body > ul.product-property-list li')
        for specification_item in specification_list:
            title = specification_item.select('.propery-title')[0].text[:-1]
            description = specification_item.select('.propery-des')[0].text
            product_dict[title] = description

        return product_dict

    def extract_product(self):
        product_html_page = self.browser.page_source
        product_data = self.extract_product_data(product_html_page)
        self.browser.back()
        return pd.Series(product_data,index= product_data.keys())