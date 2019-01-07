import pandas as pd
from selenium import webdriver
import pickle
import time
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path



def get_cookies(browser):
    browser.get("https://login.aliexpress.com/buyer.htm?return=https%3A%2F%2Fwww.aliexpress.com%2F&random=CEA73DF4D81D4775227F78080B9B6126")
    print('input your username and password in Firefox and hit Submit')
    input('Hit Enter here if you have summited the form: <Enter>')
    cookies = browser.get_cookies()
    pickle.dump(cookies, open("cookies.pickle", "wb"))


def set_cookies(browser,url):
    browser.get(url)
    cookies = pickle.load(open("cookies.pickle", "rb"))
    for cookie in cookies:
        browser.add_cookie(cookie)

    browser.add_cookie({'name':'aep_usuc_f',
                        'value':'isfm=y&site=glo&c_tp=GBP&x_alimid=814979923&isb=y&ups_u_t=1577293226431&region=UK&b_locale=en_US&ae_u_p_s=0'})
    browser.get(url)
def isProductUrl(url):
    return url.find('/store/product/')>-1

def extract_product_price(html_parser):

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

def extract_product_data(product_html_page):
    product_dict = {}
    html_parser = BeautifulSoup(product_html_page, 'html.parser')
    images = html_parser.select('#j-image-thumb-list > li > span > img')
    images_values = ''
    for image in images:
        images_values = images_values + ';' + image.get_attribute_list('src')[0]
    # images.get_attribute('src')
    product_dict['images'] = images_values[1:]
    title = html_parser.select('#j-product-detail-bd div.store-detail-main div h1.product-name')[0].text
    product_dict['title'] = title

    product_dict['price'] = extract_product_price(html_parser)

    #attributes
    attributes = html_parser.select('#j-product-info-sku > dl.p-property-item')
    number_attributes = len(attributes)
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

def extract_product(browser):
    product_html_page = browser.page_source
    product_data = extract_product_data(product_html_page)
    browser.back()
    return pd.Series(product_data,index= product_data.keys())

def extract_allproduct_in_this_page(browser,filename_to_save,number_product,dataframe):

    for product_index in range(1,number_product+1):
        all_product_pages = browser.find_elements_by_css_selector('a.pic-rind')
        #product_url = all_products_loaded_in_beatifulsoup[product_index-1].get_attribute('href')
        #allproducts.append(product_url)
        all_product_pages[product_index-1].click()
        time.sleep(3)
        product_serie = extract_product(browser)
        dataframe = dataframe.append(product_serie,ignore_index=True)

    dataframe.to_csv(filename_to_save)
    return dataframe
def count_products_in_page(html,url):
    if not isProductUrl(url):
        html_soup_parser = BeautifulSoup(html, 'html.parser')
        all_products_loaded_in_beatifulsoup = html_soup_parser.find_all('a', class_='pic-rind')
        return len(all_products_loaded_in_beatifulsoup)
    else:
        return 0

def crawling_to_findall_pages(browser,initial_url,filename_to_save):

    try:

        browser.get(initial_url)
        if(isProductUrl(browser.current_url)):
            browser.refresh()
            browser.back()

        next_button = browser.find_element_by_css_selector('div.ui-pagination-navi.util-left a.ui-pagination-next')
        isLastPage = next_button.get_attribute('class').find('disabled')>-1

        dataframe_file = Path(filename_to_save)
        if(not dataframe_file.exists()):
            dataframe = pd.DataFrame()
        else:
            dataframe = pd.read_csv(filename_to_save)

        if(isLastPage):
            number_product_in_this_page = count_products_in_page(browser.page_source,browser.current_url)
            print('allproducts loaded by beautiful: {}'.format(number_product_in_this_page))
            dataframe = extract_allproduct_in_this_page(browser,filename_to_save,number_product_in_this_page,dataframe)
            return True


        while not isLastPage:
            number_product_in_this_page = count_products_in_page(browser.page_source,browser.current_url)
            print('allproducts loaded by beautiful: {}'.format(number_product_in_this_page))
            dataframe = extract_allproduct_in_this_page(browser,filename_to_save,number_product_in_this_page,dataframe)

            next_button = browser.find_element_by_css_selector('div.ui-pagination-navi.util-left a.ui-pagination-next')
            next_button.click()
            time.sleep(2)
            next_button = browser.find_element_by_css_selector('div.ui-pagination-navi.util-left a.ui-pagination-next')
            isLastPage = next_button.get_attribute('class').find('disabled')>-1



        # Scan last page
        number_product_in_this_page = count_products_in_page(browser.page_source,browser.current_url)
        print('allproducts loaded by beautiful: {}'.format(number_product_in_this_page))
        extract_allproduct_in_this_page(browser,filename_to_save,number_product_in_this_page,dataframe)

        return True

    except Exception as e:
        return False



# do web crawling to extract all links
# for each page extract all product links
# extract the data for each product link

initial_url_pattern = 'https://www.aliexpress.com/store/group/Home-decoration/1225042_500909156/28.html?spm=2114.12010612.8148361.11.5ff754d0eMvqWs&origin=n&SortType=bestmatch_sort&g=y'
#url = 'https://www.glassdoor.co.uk/Reviews/uk-reviews-SRCH_IL.0,2_IN2_IP5210.htm'
#try:
browser = webdriver.Chrome('/Users/martarey/dev/python/ml_course1/chromedriver')
# cap = DesiredCapabilities().FIREFOX
# cap["marionette"] = False
# browser = webdriver.Firefox(capabilities=cap, executable_path='/Users/martarey/dev/python/ml_course1/geckodriver')

browser.implicitly_wait(15)
get_cookies(browser)

initial_url = initial_url_pattern.replace('{page}','')
set_cookies(browser, initial_url)
allfiles_used = []
got_to_end = False
while not got_to_end:
    allfiles_used.append('home-decoration.csv')
    got_to_end = crawling_to_findall_pages(browser,initial_url,'home-decoration.csv')
    initial_url = browser.current_url

browser.quit()


